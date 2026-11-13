"""Explicit acquisition only. Analysis never calls the network. Resume uses cached bytes."""
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from config import ROOT, INDICATORS, ensure_dirs

API = 'https://api.worldbank.org/v2/'

def fetch(url, path):
    receipt = path.with_suffix(path.suffix + '.receipt.json')
    if path.exists() and receipt.exists():
        raw = path.read_bytes()
        info = json.loads(receipt.read_text('utf-8'))
        if hashlib.sha256(raw).hexdigest() != info['sha256']:
            raise ValueError(f'Cache checksum mismatch: {path}')
        return raw, info
    error = None
    for attempt in range(4):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'UniversityPopulationAgingResearch/1.0'})
            with urllib.request.urlopen(request, timeout=90) as response:
                raw = response.read()
            info = {'url': url, 'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw), 'path': str(path.relative_to(ROOT)).replace('\\', '/')}
            path.write_bytes(raw)
            receipt.write_text(json.dumps(info, indent=2), 'utf-8')
            return raw, info
        except Exception as exc:
            error = exc
            if attempt < 3:
                time.sleep(2 ** attempt)
    raise RuntimeError(f'Download failed after 4 attempts: {url}: {error}')

def paginated(endpoint, stem, params=''):
    all_rows, receipts = [], []
    page, pages, expected = 1, 1, None
    while page <= pages:
        url = f'{API}{endpoint}?format=json&per_page=2000&page={page}' + ('&' + params if params else '')
        raw, info = fetch(url, ROOT / 'data/raw' / f'{stem}_p{page}.json')
        payload = json.loads(raw)
        if not isinstance(payload, list) or len(payload) != 2 or not isinstance(payload[0], dict) or 'pages' not in payload[0]:
            raise ValueError(f'Invalid API response: {url}: {str(payload)[:300]}')
        header, rows = payload
        pages = int(header['pages'])
        if expected is None:
            expected = int(header['total'])
        if int(header['total']) != expected:
            raise ValueError('API total changed during pagination; use a fresh snapshot directory')
        all_rows.extend(rows or [])
        receipts.append(info | {'api_header': header})
        page += 1
    if len(all_rows) != expected:
        raise ValueError(f'Incomplete pagination for {stem}: {len(all_rows)} != {expected}')
    return receipts

def collect_indicator(item):
    name, code = item
    receipts = paginated('indicator/' + code, 'metadata_' + name, 'source=2')
    # Full published range lets metadata coverage be computed, then analysis restricts 1991–2023.
    receipts += paginated('country/all/indicator/' + code, name, 'source=2')
    receipts += paginated('country/VNM/indicator/' + code, 'verify_' + name, 'source=2&date=1991:2023')
    _, glossary_receipt = fetch('https://databank.worldbank.org/metadataglossary/world-development-indicators/series/' + code, ROOT / 'data/raw' / ('glossary_' + name + '.html'))
    receipts.append(glossary_receipt)
    print(f'Cached {code}', flush=True)
    return receipts

def main():
    ensure_dirs()
    receipts = paginated('country', 'countries')
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(collect_indicator, INDICATORS.items()):
            receipts.extend(result)
    raw, info = fetch('https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip', ROOT / 'data/raw/natural_earth_countries.zip')
    receipts.append(info)
    snapshot_id = hashlib.sha256(''.join(sorted(r['sha256'] for r in receipts)).encode()).hexdigest()[:16]
    manifest = {'snapshot_id': snapshot_id, 'created_utc': datetime.now(timezone.utc).isoformat(), 'analysis_period': [1991, 2023], 'interface': 'World Bank WDI source 2', 'license': 'World Bank CC BY 4.0 with additional terms; Natural Earth public domain', 'license_urls': ['https://data.worldbank.org/summary-terms-of-use', 'https://www.naturalearthdata.com/about/terms-of-use/'], 'files': receipts}
    (ROOT / 'data/metadata/source_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), 'utf-8')
    print(f'Snapshot {snapshot_id}: {len(receipts)} cached responses/files', flush=True)

if __name__ == '__main__':
    main()
