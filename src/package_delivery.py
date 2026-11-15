"""Portable archive with a verified SHA256 manifest; standard library only."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from pathlib import PurePosixPath
import tempfile
import zipfile

EXCLUDED_DIRS = {'work', 'history', '.venv', 'venv', '__pycache__', '.git', '.pbi', '.pytest_cache', '.ruff_cache', '.ipynb_checkpoints', 'node_modules', '.idea'}
MANIFEST = 'delivery-manifest.json'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def deliverable_files(root):
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in rel.parts) or path.is_symlink():
            continue
        private = path.name == '.env' or path.name.startswith('.env.') or path.name in {'credentials.json', 'id_rsa', 'id_ed25519'}
        # Raw geography and test fixtures may legitimately be ZIP sources.
        release_archive = path.suffix.lower() == '.zip' and rel.parts[0] not in {'data', 'tests'}
        if path.is_file() and not private and not release_archive and path.name != MANIFEST and not path.name.startswith('~$') and path.suffix.lower() not in {'.pyc', '.tmp', '.log', '.pem', '.key'}:
            yield path

def safe_relative(name):
    """Reject paths that could escape the archive's single project directory."""
    if not isinstance(name, str):
        raise ValueError('Unsafe manifest path: ' + str(name))
    path = PurePosixPath(name)
    if not name or '\\' in name or ':' in name or path.is_absolute() or '..' in path.parts or path.as_posix() != name:
        raise ValueError('Unsafe manifest path: ' + str(name))
    return name

def verify_archive(archive):
    try:
        return _verify_archive(archive)
    except (zipfile.BadZipFile, KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError('Invalid delivery archive: ' + str(exc)) from exc

def _verify_archive(archive):
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError('ZIP CRC check failed')
        names = z.namelist()
        manifests = [n for n in names if n.count('/') == 1 and n.endswith('/' + MANIFEST)]
        if len(manifests) != 1 or len(names) != len(set(names)):
            raise ValueError('Missing/ambiguous manifest or duplicate ZIP entries')
        prefix = manifests[0].split('/')[0] + '/'
        safe_relative(prefix[:-1])
        manifest = json.loads(z.read(manifests[0]))
        if manifest.get('schema_version') != 1 or not isinstance(manifest.get('files'), list):
            raise ValueError('Unsupported manifest schema')
        paths = [safe_relative(item['path']) for item in manifest['files']]
        if len(paths) != len(set(paths)):
            raise ValueError('Duplicate manifest paths')
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
    if not root.is_dir():
        raise ValueError('Project directory does not exist')
    output = Path(output).resolve() if output else root.parent / (root.name + '-complete.zip')
    if output == root or root in output.parents:
        raise ValueError('ZIP output must be outside project directory')
    files = list(deliverable_files(root))
    manifest = {'schema_version': 1, 'created_at_utc': datetime.now(timezone.utc).isoformat(),
                'note': 'Manifest excludes itself to avoid recursive hashing; work/runtime/cache files excluded.',
                'files': [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())} for p in files]}
    output.parent.mkdir(parents=True, exist_ok=True)
    # A unique temporary file prevents concurrent releases from clobbering one another.
    with tempfile.NamedTemporaryFile(prefix=output.stem + '-', suffix='.zip.tmp', dir=output.parent, delete=False) as temp:
        temporary = Path(temp.name)
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for path in files:
                z.write(path, root.name + '/' + path.relative_to(root).as_posix())
            z.writestr(root.name + '/' + MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        count = verify_archive(temporary)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return {'archive': str(output), 'files': count, 'bytes': output.stat().st_size, 'sha256': digest(output.read_bytes()), 'verified': True}
