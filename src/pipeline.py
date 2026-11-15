"""Offline orchestration with explicit optional regeneration and audit logs."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
from importlib import metadata
import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from config import ROOT

LOG = logging.getLogger('aging')
CORE = ('pandas', 'numpy', 'matplotlib', 'plotly', 'shapefile', 'nbformat')
OPTIONAL = ('nbclient', 'nbconvert', 'ipykernel')

def doctor():
    modules = {n: importlib.util.find_spec(n) is not None for n in (*CORE, *OPTIONAL)}
    distributions = {name: ('pyshp' if name == 'shapefile' else name) for name in modules}
    versions = {}
    for name, distribution in distributions.items():
        try:
            versions[name] = metadata.version(distribution)
        except metadata.PackageNotFoundError:
            versions[name] = None
    result = {'python': sys.version.split()[0], 'python_executable': sys.executable,
              'python_supported': sys.version_info >= (3, 12), 'modules': modules, 'versions': versions,
              'missing_core': [n for n in CORE if not modules[n]],
              'missing_notebook_extras': [n for n in OPTIONAL if not modules[n]],
              'install_core': 'python -m pip install -r requirements-core.txt',
              'install_notebook_extras': 'python -m pip install -r requirements.txt',
              'powershell': shutil.which('pwsh') or shutil.which('powershell'),
              'word_pdf': 'Requires Windows and installed Microsoft Word; doctor does not launch Word',
              'source_manifest_exists': (ROOT / 'data/metadata/source_manifest.json').is_file()}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['python_supported'] and not result['missing_core'] and result['source_manifest_exists'] else 1

class Runner:
    def __init__(self, root=ROOT, env=None):
        self.root = Path(root)
        self.env = dict(os.environ if env is None else env)
        self.work = Path(self.env.setdefault('PROJECT_WORK', str(self.root / 'work')))
        self.log_root = self.work / 'logs'
        self.logs = self.log_root / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
        self.logs.mkdir(parents=True, exist_ok=True)
        for key, subdir in [('MPLCONFIGDIR', 'mpl'), ('JUPYTER_RUNTIME_DIR', 'jupyter-runtime'), ('IPYTHONDIR', 'ipython')]:
            self.env.setdefault(key, str(self.work / subdir))
        self.receipt = {'started_at_utc': datetime.now(timezone.utc).isoformat(), 'python': sys.executable, 'steps': [], 'status': 'running'}

    def save(self):
        content = json.dumps(self.receipt, ensure_ascii=False, indent=2)
        (self.logs / 'build-receipt.json').write_text(content, encoding='utf-8')
        (self.log_root / 'build-receipt.json').write_text(content, encoding='utf-8')

    def run(self, name, command, extra_env=None):
        log_path = self.logs / f'{name}.log'
        step = {'name': name, 'command': [str(x) for x in command], 'log': str(log_path)}
        self.receipt['steps'].append(step)
        started = time.perf_counter()
        LOG.info('Running %s', name)
        try:
            with log_path.open('w', encoding='utf-8') as log:
                subprocess.run(command, cwd=self.root, env={**self.env, **(extra_env or {})}, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=120 if name == 'word_pdf' else None)
            step['status'] = 'passed'
        except (subprocess.SubprocessError, OSError) as exc:
            step.update(status='failed', error=str(exc))
            self.receipt['status'] = 'failed'
            LOG.error('%s failed. See %s', name, log_path)
            if log_path.exists():
                LOG.error('Last output:\n%s', log_path.read_text(encoding='utf-8', errors='replace')[-2000:])
            raise
        finally:
            step['seconds'] = round(time.perf_counter() - started, 3)
            self.save()
        LOG.info('%s passed (%.1fs)', name, step['seconds'])

    def script(self, name, **kwargs):
        self.run(Path(name).stem, [sys.executable, str(self.root / 'src' / name)], **kwargs)

    def finish(self):
        if self.receipt['status'] == 'failed':
            raise RuntimeError('Cannot mark a failed run as passed')
        self.receipt.update(status='passed', finished_at_utc=datetime.now(timezone.utc).isoformat())
        self.save()
        LOG.info('Completed. Receipt: %s', self.logs / 'build-receipt.json')

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None

def build(args):
    runner = Runner()
    master = ROOT / 'data/processed/master.csv'
    before = sha256(master)
    if args.pdf == 'word':
        shell = shutil.which('pwsh') or shutil.which('powershell')
        if os.name != 'nt' or not shell:
            raise RuntimeError('--pdf word requires PowerShell and Microsoft Word on Windows')
    if args.acquire:
        runner.script('acquire.py')
    for name in ('prepare.py', 'analyze.py', 'visualize.py', 'export_evidence.py', 'explore.py'):
        runner.script(name)
    after = sha256(master)
    runner.receipt['master_csv'] = {'before_sha256': before, 'after_sha256': after, 'identical': before == after if before else None}
    if args.notebook:
        runner.script('notebook.py', extra_env={'AGING_REUSE_RESULTS': '1'})
    if args.pdf == 'word':
        runner.run('word_pdf', [shell, '-NoProfile', '-File', str(ROOT / 'src/export_word_pdf.ps1')])
    runner.run('tests', [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
    runner.script('verify_delivery.py')
    runner.finish()
    LOG.info('Authored report, Canva presentation and saved PBIX retained; review them when analysis changes.')

def main(argv=None):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or (argv[0].startswith('--') and argv[0] != '--help'):
        argv.insert(0, 'build')
    parser = argparse.ArgumentParser(description='Population aging: offline build, validation and packaging')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('doctor', help='Inspect dependencies without installing or downloading')
    b = commands.add_parser('build', help='Rebuild data, charts and web dashboard; retain authored Word report')
    b.add_argument('--acquire', action='store_true', help='Explicitly fetch/resume cached source downloads')
    b.add_argument('--notebook', action='store_true', help='Fresh kernel; reuse freshly built outputs')
    b.add_argument('--pdf', choices=('none', 'word'), default='none')
    commands.add_parser('check', help='Run tests and cross-artifact validation')
    commands.add_parser('powerbi', help='Rebuild editable native PBIP; close the project in Desktop first')
    p = commands.add_parser('package', help='Validate, create manifest and verify portable ZIP')
    p.add_argument('--output', type=Path, help='ZIP outside project; default sibling population-aging-complete.zip')
    v = commands.add_parser('verify-archive', help='Check a downloaded ZIP against its embedded SHA256 manifest')
    v.add_argument('archive', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == 'doctor':
            return doctor()
        if args.command == 'verify-archive':
            from package_delivery import verify_archive
            print(json.dumps({'archive': str(args.archive), 'files': verify_archive(args.archive), 'verified': True}))
            return 0
        if args.command == 'build':
            build(args)
        elif args.command == 'powerbi':
            runner = Runner()
            runner.script('build_powerbi.py')
            runner.finish()
        else:
            runner = Runner()
            runner.run('tests', [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
            runner.script('verify_delivery.py')
            if args.command == 'package':
                from package_delivery import package
                try:
                    print(json.dumps(package(ROOT, args.output), ensure_ascii=False, indent=2))
                except (OSError, ValueError) as exc:
                    runner.receipt.update(status='failed',error=str(exc))
                    runner.save()
                    raise
            runner.finish()
        return 0
    except (subprocess.SubprocessError, OSError, RuntimeError, ValueError) as exc:
        LOG.error('%s', exc)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
