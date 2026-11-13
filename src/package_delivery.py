"""Portable archive with a verified SHA256 manifest; standard library only."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import zipfile

EXCLUDED_DIRS = {'work', 'history', '.venv', 'venv', '__pycache__', '.git', '.pbi', '.pytest_cache', '.ipynb_checkpoints', 'node_modules'}
MANIFEST = 'delivery-manifest.json'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def deliverable_files(root):
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in rel.parts) or path.is_symlink():
            continue
        if path.is_file() and path.name != MANIFEST and not path.name.startswith('~$') and path.suffix not in {'.pyc', '.tmp', '.lock'}:
            yield path

def verify_archive(archive):
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError('ZIP CRC check failed')
        names = z.namelist()
        manifests = [n for n in names if n.count('/') == 1 and n.endswith('/' + MANIFEST)]
        if len(manifests) != 1 or len(names) != len(set(names)):
            raise ValueError('Missing/ambiguous manifest or duplicate ZIP entries')
        prefix = manifests[0].split('/')[0] + '/'
        manifest = json.loads(z.read(manifests[0]))
        expected = {prefix + item['path'] for item in manifest['files']} | {manifests[0]}
        if set(names) != expected:
            raise ValueError('ZIP entries differ from manifest')
        for item in manifest['files']:
            data = z.read(prefix + item['path'])
            if len(data) != item['bytes'] or digest(data) != item['sha256']:
                raise ValueError('Checksum mismatch: ' + item['path'])
    return len(manifest['files'])

def package(root, output=None):
    root = Path(root).resolve()
    output = Path(output).resolve() if output else root.parent / (root.name + '-complete.zip')
    if output == root or root in output.parents:
        raise ValueError('ZIP output must be outside project directory')
    files = list(deliverable_files(root))
    manifest = {'schema_version': 1, 'created_at_utc': datetime.now(timezone.utc).isoformat(),
                'note': 'Manifest excludes itself to avoid recursive hashing; work/runtime/cache files excluded.',
                'files': [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())} for p in files]}
    manifest_path = root / MANIFEST
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix('.zip.tmp')
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for path in files + [manifest_path]:
                z.write(path, root.name + '/' + path.relative_to(root).as_posix())
        count = verify_archive(temporary)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return {'archive': str(output), 'files': count, 'bytes': output.stat().st_size, 'sha256': digest(output.read_bytes()), 'verified': True}
