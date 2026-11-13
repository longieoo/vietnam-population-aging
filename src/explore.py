"""Offline explorer using Plotly's supported HTML serializer and a small UI template."""
import json
import hashlib
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from config import ROOT, FOCAL, COLORS


def main():
    df = pd.read_csv(ROOT / 'data/processed/master.csv')
    base = json.loads((ROOT / 'data/metadata/price_base.json').read_text('utf-8'))['year']
    snapshot = json.loads((ROOT / 'data/metadata/source_manifest.json').read_text('utf-8'))['snapshot_id']
    df['aging_index'] = df.age_65_plus.div(df.age_0_14.where(df.age_0_14.gt(0))).mul(100)
    df['potential_support_ratio'] = df.age_15_64.div(df.age_65_plus.where(df.age_65_plus.gt(0)))
    crossings = pd.read_csv(ROOT / 'outputs/tables/threshold_crossings.csv')
    with (ROOT / 'data/processed/master.csv').open('rb') as source:
        master_sha = hashlib.file_digest(source, 'sha256').hexdigest()
    payload = {'rows': json.loads(df.to_json(orient='records', force_ascii=False, double_precision=15)),
               'crossings': json.loads(crossings.to_json(orient='records', force_ascii=False, double_precision=15)),
               'names': FOCAL, 'colors': COLORS, 'snapshot': snapshot, 'price_base': base,
               'master_sha256': master_sha, 'window': [1991, 2023]}
    # Script JSON is escaped separately; never replace tokens inside Plotly JS.
    encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False).replace('<', '\\u003c')
    html = Path(__file__).with_name('dashboard_template.html').read_text('utf-8')
    html = html.replace('__SNAPSHOT__', snapshot).replace('__BASE__', str(base)).replace('__DATA__', encoded)
    html = html.replace('__MODEL__', Path(__file__).with_name('dashboard_model.js').read_text('utf-8'))
    html = html.replace('__APP__', Path(__file__).with_name('dashboard_app.js').read_text('utf-8'))
    plot = pio.to_html(go.Figure(), include_plotlyjs=True, full_html=False, div_id='chart', config={'responsive': True, 'displaylogo': False})
    html = html.replace('__PLOT__', plot)
    target = ROOT / 'outputs/interactive/explorer.html'
    target.write_text(html, encoding='utf-8')
    (ROOT / 'outputs/tables/dashboard_data.json').write_text(encoded + '\n', encoding='utf-8')
    # Direct file fallbacks for browsers that restrict Blob downloads.
    for name, fields in [('gdp', ['gdp_ppp', 'age_65_plus']), ('labor', ['age_15_64', 'employment'])]:
        sample = df.loc[df.year.eq(2023)].dropna(subset=fields)
        sample[['iso3', 'country', 'year', *fields]].to_csv(
            ROOT / f'outputs/tables/dashboard_{name}_2023.csv', index=False, encoding='utf-8-sig')
    df[['iso3', 'country', 'year', 'age_65_plus', 'age_0_14', 'age_15_64',
        'aging_index', 'potential_support_ratio']].to_csv(
            ROOT / 'outputs/tables/dashboard_aging_metrics.csv', index=False, encoding='utf-8-sig')
    print(f'Wrote offline explorer: {target.stat().st_size:,} bytes')


if __name__ == '__main__':
    main()
