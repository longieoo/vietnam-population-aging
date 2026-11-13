"""Deterministic offline cleaning, feature generation, and coverage audit."""
import hashlib
import json
import re
import numpy as np
import pandas as pd
from config import ROOT, INDICATORS, YEARS, ensure_dirs

def require(condition, message):
    """Data-integrity checks must stay active under python -O."""
    if not condition:
        raise ValueError(message)

def read_pages(stem):
    files = sorted((p for p in (ROOT / 'data/raw').glob(stem + '_p*.json') if re.fullmatch(re.escape(stem) + r'_p\d+\.json', p.name)), key=lambda p: int(p.stem.rsplit('p', 1)[1]))
    if not files:
        raise FileNotFoundError(f'No cached pages for {stem}; run acquire.py explicitly')
    payloads = [json.loads(p.read_text('utf-8')) for p in files]
    require(len(payloads) == int(payloads[0][0]['pages']), f'Incomplete pages: {stem}')
    require([int(p[0]['page']) for p in payloads] == list(range(1,len(payloads)+1)), f'Nonconsecutive pages: {stem}')
    rows = [row for payload in payloads for row in (payload[1] or [])]
    require(len(rows) == int(payloads[0][0]['total']), f'Unexpected row count: {stem}')
    return rows

def verify_snapshot():
    manifest = json.loads((ROOT / 'data/metadata/source_manifest.json').read_text('utf-8'))
    for item in manifest['files']:
        with (ROOT / item['path']).open('rb') as source:
            actual = hashlib.file_digest(source, 'sha256').hexdigest()
        require(actual == item['sha256'], f'Snapshot checksum mismatch: {item["path"]}')
    return manifest

def add_features(frame):
    out = frame.copy()
    denominator = out.age_15_64.where(out.age_15_64 > 0)
    out['population_65_plus'] = out.population * out.age_65_plus / 100
    out['child_dependency'] = out.age_0_14 / denominator * 100
    out['old_dependency'] = out.age_65_plus / denominator * 100
    out['total_dependency'] = out.child_dependency + out.old_dependency
    return out

def first_crossing(frame, threshold=10):
    """First observed above, requiring a prior below; missing years imply an interval."""
    valid = frame.dropna(subset=['age_65_plus']).sort_values('year')
    require(not frame.year.duplicated().any(), 'Duplicate years in threshold series')
    result = {'threshold': threshold, 'status': 'no_data', 'year': None, 'previous_year': None, 'gdp_ppp': None, 'share': None}
    if valid.empty:
        return result
    if valid.iloc[0].age_65_plus >= threshold:
        return result | {'status': 'already_above', 'share': float(valid.iloc[0].age_65_plus)}
    above = valid[valid.age_65_plus >= threshold]
    if above.empty:
        return result | {'status': 'not_reached'}
    row = above.iloc[0]
    previous = valid[valid.year < row.year].iloc[-1]
    # Also flag any earlier missing years: a crossing and reversal could be hidden.
    missing_before = valid.iloc[0].year > frame.year.min() or valid[valid.year <= row.year].year.diff().dropna().ne(1).any()
    status = 'gap_uncertain' if missing_before else 'observed'
    return result | {'status': status, 'year': int(row.year), 'previous_year': int(previous.year), 'gdp_ppp': float(row.gdp_ppp) if pd.notna(row.gdp_ppp) else None, 'share': float(row.age_65_plus)}

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=lambda x: x.item() if hasattr(x, 'item') else str(x)), 'utf-8')

def main():
    ensure_dirs()
    manifest = verify_snapshot()
    meta = read_pages('countries')
    countries = pd.DataFrame([{'iso3': r['id'], 'country': r['name'], 'region': r['region']['value'], 'income_group': r['incomeLevel']['value'], 'is_aggregate': r['region']['id'] == 'NA' or r['region']['value'] == 'Aggregates'} for r in meta])
    require(not countries.iso3.duplicated().any(), 'Data validation failed: not countries.iso3.duplicated().any()')
    countries.to_csv(ROOT / 'data/metadata/countries.csv', index=False)
    eligible = countries.loc[~countries.is_aggregate]
    tables, dictionary, all_ranges = [], [], []
    for variable, code in INDICATORS.items():
        rows = read_pages(variable)
        frame = pd.DataFrame([{'iso3': r['countryiso3code'], 'year': int(r['date']), variable: r['value']} for r in rows])
        frame[variable] = pd.to_numeric(frame[variable], errors='raise')
        frame = frame[frame.iso3.isin(eligible.iso3)]
        require(not frame.duplicated(['iso3', 'year']).any(), variable)
        available = frame.dropna(subset=[variable])
        metadata = read_pages('metadata_' + variable)[0]
        dictionary.append({'variable': variable, 'code': code, **metadata, 'available_year_min': int(available.year.min()), 'available_year_max': int(available.year.max()), 'economies_any_year': int(available.iso3.nunique()), 'observed_rows_full_published_range': len(available)})
        all_ranges.append(available.groupby('iso3').year.agg(['min', 'max', 'count']).reset_index().assign(variable=variable))
        tables.append(frame[frame.year.isin(YEARS)])
    master = tables[0]
    for table in tables[1:]:
        master = master.merge(table, on=['iso3', 'year'], how='outer', validate='one_to_one')
    master = master.dropna(subset=list(INDICATORS), how='all').merge(eligible.drop(columns='is_aggregate'), on='iso3', how='left', validate='many_to_one')
    master = master.sort_values(['iso3', 'year']).reset_index(drop=True)
    require(not master.duplicated(['iso3', 'year']).any(), "Data validation failed: not master.duplicated(['iso3', 'year']).any()")
    require(master.year.between(1991, 2023).all() and master.iso3.isin(eligible.iso3).all(), 'Data validation failed: master.year.between(1991, 2023).all() and master.iso3.isin(eligible.iso3).all()')
    errors = []
    for col in ['age_0_14', 'age_15_64', 'age_65_plus', 'lfpr', 'employment']:
        if not master[col].dropna().between(0, 100).all():
            errors.append('range_' + col)
    for col in ['population', 'gdp_ppp']:
        if not master[col].dropna().gt(0).all(): errors.append('positive_' + col)
    if not master.fertility.dropna().between(0, 12).all(): errors.append('fertility_range')
    age_cols = ['age_0_14', 'age_15_64', 'age_65_plus']
    age_error = master[age_cols].sum(axis=1, min_count=3).sub(100).abs()
    if age_error.gt(0.15).any(): errors.append('age_sum')
    if (master.employment - master.lfpr).gt(0.05).any(): errors.append('employment_exceeds_lfpr')
    require(not errors, f'Invalid source values: {errors}')
    master = add_features(master)
    master.to_csv(ROOT / 'data/processed/master.csv', index=False, float_format='%.12g')
    pd.concat(all_ranges).to_csv(ROOT / 'data/metadata/full_published_coverage.csv', index=False)
    write_json(ROOT / 'data/metadata/indicator_metadata.json', dictionary)
    gdp_title = next(d['name'] for d in dictionary if d['variable'] == 'gdp_ppp')
    price_base = re.search(r'constant (\d{4})', gdp_title)
    if not price_base: raise ValueError('Cannot verify PPP price base from metadata: ' + gdp_title)
    write_json(ROOT / 'data/metadata/price_base.json', {'year': int(price_base.group(1)), 'official_title': gdp_title})
    missing = master[list(INDICATORS)].isna()
    pd.DataFrame({'variable': list(INDICATORS), 'missing': missing.sum().values, 'available': (~missing).sum().values, 'missing_percent': missing.mean().values * 100}).to_csv(ROOT / 'outputs/tables/missingness_indicator.csv', index=False)
    for group in ['iso3', 'year']:
        missing.assign(**{group: master[group]}).groupby(group).mean().mul(100).to_csv(ROOT / f'outputs/tables/missingness_{group}.csv')
    jumps = []
    thresholds = {'age_0_14': 2, 'age_15_64': 2, 'age_65_plus': 1.5, 'lfpr': 5, 'employment': 5, 'fertility': 0.5}
    for col, limit in thresholds.items():
        change = master.groupby('iso3')[col].diff()
        consecutive = master.groupby('iso3').year.diff().eq(1)
        selected = master.loc[change.abs().gt(limit) & consecutive, ['iso3', 'country', 'year', col]].copy()
        selected['variable'], selected['change'], selected['review_threshold'] = col, change[selected.index], limit
        selected.rename(columns={col: 'value'}, inplace=True)
        jumps.append(selected)
    growth = master.groupby('iso3').gdp_ppp.pct_change(fill_method=None).mul(100)
    selected = master.loc[growth.abs().gt(20) & master.groupby('iso3').year.diff().eq(1), ['iso3', 'country', 'year', 'gdp_ppp']].rename(columns={'gdp_ppp':'value'}).copy()
    selected['variable'], selected['change'], selected['review_threshold'] = 'gdp_ppp', growth[selected.index], 20
    jumps.append(selected)
    pd.concat(jumps, ignore_index=True).to_csv(ROOT / 'outputs/tables/abrupt_changes.csv', index=False)
    official_checks = []
    for var in INDICATORS:
        for r in read_pages('verify_' + var):
            if int(r['date']) not in [1991, 2023] or r['value'] is None: continue
            actual = master.loc[(master.iso3 == 'VNM') & (master.year == int(r['date'])), var].iloc[0]
            official_checks.append({'variable': var, 'year': int(r['date']), 'official': r['value'], 'processed': actual, 'matches': bool(np.isclose(actual, r['value'], rtol=1e-10))})
    pd.DataFrame(official_checks).to_csv(ROOT / 'outputs/tables/vietnam_source_checks.csv', index=False)
    require(all(c['matches'] for c in official_checks), "Data validation failed: all(c['matches'] for c in official_checks)")
    summary = {'snapshot_id': manifest['snapshot_id'], 'economies': master.iso3.nunique(), 'meaningful_rows': len(master), 'complete_age_shares': int(master[age_cols].notna().all(axis=1).sum()), 'complete_demographic_rows': int(master[['population', *age_cols, 'fertility']].notna().all(axis=1).sum()), 'aging_gdp_rows': int(master[['age_65_plus','gdp_ppp']].notna().all(axis=1).sum()), 'working_age_employment_rows': int(master[['age_15_64','employment']].notna().all(axis=1).sum()), 'labor_both_rows': int(master[['lfpr','employment']].notna().all(axis=1).sum()), 'all_eight_complete_rows': int(master[list(INDICATORS)].notna().all(axis=1).sum()), 'year_min': int(master.year.min()), 'year_max': int(master.year.max()), 'aggregate_entities_excluded': int(countries.is_aggregate.sum()), 'empty_eligible_entities': sorted(set(eligible.iso3) - set(master.iso3)), 'age_sum_max_absolute_error_pp': float(age_error.max()), 'age_sum_tolerance_pp': 0.15, 'range_errors': errors, 'source_checks': len(official_checks), 'price_base': int(price_base.group(1))}
    write_json(ROOT / 'outputs/tables/quality_summary.json', summary)
    require(not errors, errors)
    require(len(master) >= 5000, 'Fewer than 5000 meaningful observations')
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return master

if __name__ == '__main__': main()
