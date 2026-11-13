"""Analysis-specific samples, endpoint comparisons and descriptive robustness."""
import json
import numpy as np
import pandas as pd
from config import ROOT, FOCAL
from prepare import first_crossing, write_json

def demographic_insights(frame):
    """Endpoint identities, not causal estimates or extrapolated forecasts."""
    vn=frame.loc[frame.iso3.eq('VNM')].set_index('year')
    a,b=vn.loc[1991],vn.loc[2023]
    base=vn.loc[2010]
    peak=vn.loc[int(vn.age_15_64.idxmax())]
    # Symmetric decomposition of N=P*s: average the two possible orders.
    p0,p1=a.population,b.population
    s0,s1=a.age_65_plus/100,b.age_65_plus/100
    population_component=(p1-p0)*(s0+s1)/2
    age_structure_component=(s1-s0)*(p0+p1)/2
    total=b.population_65_plus-a.population_65_plus
    all_end=frame.loc[frame.year.eq(2023)].set_index('iso3')
    recent_global=(all_end.age_65_plus-frame.loc[frame.year.eq(2010)].set_index('iso3').age_65_plus)/13
    result={
        'recent_start':2010,'recent_end':2023,
        'earlier_annual_change_pp':float((base.age_65_plus-a.age_65_plus)/19),
        'recent_annual_change_pp':float((b.age_65_plus-base.age_65_plus)/13),
        'global_recent_median_annual_change_pp':float(recent_global.median()),
        'global_recent_economies':int(recent_global.notna().sum()),
        'recent_aging_change_pp':float(b.age_65_plus-base.age_65_plus),
        'recent_fraction_of_full_change_pct':float((b.age_65_plus-base.age_65_plus)/(b.age_65_plus-a.age_65_plus)*100),
        'working_age_decline_since_peak_pp':float(b.age_15_64-peak.age_15_64),
        'dependency_increase_since_min':float(b.total_dependency-vn.total_dependency.min()),
        'old_dependency_increase_since_peak':float(b.old_dependency-peak.old_dependency),
        'child_dependency_increase_since_peak':float(b.child_dependency-peak.child_dependency),
        'old_dependency_fraction_of_rebound_pct':float((b.old_dependency-peak.old_dependency)/(b.total_dependency-peak.total_dependency)*100),
        'lfpr_change_2019_2023_pp':float(b.lfpr-vn.loc[2019,'lfpr']),
        'employment_change_2019_2023_pp':float(b.employment-vn.loc[2019,'employment']),
        'older_population_increase':float(total),
        'population_component':float(population_component),
        'age_structure_component':float(age_structure_component),
        'age_structure_component_pct':float(age_structure_component/total*100),
        'definition':'Symmetric two-factor accounting decomposition; not causal attribution',
        'gdp_sample_population_coverage_pct':float(all_end.loc[all_end.gdp_ppp.notna(),'population'].sum()/all_end.population.sum()*100),
        'labor_sample_population_coverage_pct':float(all_end.loc[all_end.employment.notna(),'population'].sum()/all_end.population.sum()*100),
    }
    return result

def main():
    df = pd.read_csv(ROOT / 'data/processed/master.csv')
    out = ROOT / 'outputs/tables'
    focal = df[df.iso3.isin(FOCAL)].copy()
    focal.to_csv(out / 'focal_series.csv', index=False)
    start = df[df.year.eq(1991)].set_index('iso3')
    end = df[df.year.eq(2023)].set_index('iso3')
    endpoints = start[['country','age_65_plus','gdp_ppp','population']].join(end[['age_65_plus','gdp_ppp','population']], how='inner', lsuffix='_1991', rsuffix='_2023')
    endpoints['aging_change_pp'] = endpoints.age_65_plus_2023 - endpoints.age_65_plus_1991
    endpoints['gdp_change_percent'] = (endpoints.gdp_ppp_2023 / endpoints.gdp_ppp_1991 - 1) * 100
    endpoints.to_csv(out / 'endpoints.csv')
    crossings = []
    for code, group in df.groupby('iso3'):
        for threshold in [8,10,12]:
            crossings.append({'iso3': code, 'country': group.country.iloc[0], **first_crossing(group, threshold)})
    crossings = pd.DataFrame(crossings)
    crossings.to_csv(out / 'threshold_crossings.csv', index=False)
    periods = []
    for a,b in [(1991,2000),(2000,2010),(2010,2023)]:
        a_df = df[df.year.eq(a)].set_index('iso3')
        b_df = df[df.year.eq(b)].set_index('iso3')
        changes = b_df.age_65_plus.sub(a_df.age_65_plus).dropna()
        periods.extend({'iso3': code, 'period': f'{a}–{b}', 'change_pp': val, 'annual_change_pp': val/(b-a)} for code,val in changes.items())
    pd.DataFrame(periods).to_csv(out / 'period_changes.csv', index=False)
    samples = {'aging_2023': end.dropna(subset=['age_65_plus']), 'gdp_aging_2023': end.dropna(subset=['age_65_plus','gdp_ppp']), 'labor_2023': end.dropna(subset=['age_15_64','employment']), 'balanced_aging_endpoints': endpoints.dropna(subset=['age_65_plus_1991','age_65_plus_2023'])}
    for name, data in samples.items(): data.to_csv(out / (name + '.csv'))
    robust = []
    for name, a, b, log in [('gdp_aging_2023','gdp_ppp','age_65_plus',True),('labor_2023','age_15_64','employment',False)]:
        sample = samples[name]
        for restriction in ['all','trim_5_95','exclude_population_under_1m']:
            sub = sample.copy()
            if restriction == 'trim_5_95':
                sub = sub[sub[a].between(sample[a].quantile(.05),sample[a].quantile(.95)) & sub[b].between(sample[b].quantile(.05),sample[b].quantile(.95))]
            elif restriction == 'exclude_population_under_1m':
                sub = sub[sub.population.ge(1e6)]
            x = np.log(sub[a]) if log else sub[a]
            robust.append({'analysis': name, 'restriction': restriction, 'n':len(sub), 'pearson':x.corr(sub[b]), 'spearman':sub[a].rank().corr(sub[b].rank()), 'x_transform':'natural_log' if log else 'none'})
    pd.DataFrame(robust).to_csv(out / 'robustness.csv', index=False)
    balanced = samples['balanced_aging_endpoints'].dropna(subset=['population_1991','population_2023'])
    summaries = []
    for year in [1991,2023]:
        val, weight = balanced[f'age_65_plus_{year}'], balanced[f'population_{year}']
        summaries.append({'year':year,'n':len(balanced),'unweighted_mean':val.mean(),'median':val.median(),'q25':val.quantile(.25),'q75':val.quantile(.75),'population_weighted_mean':np.average(val,weights=weight)})
    pd.DataFrame(summaries).to_csv(out / 'global_distribution.csv', index=False)
    vn = focal[focal.iso3.eq('VNM')].set_index('year')
    summary = {'vietnam_1991':vn.loc[1991].drop(labels=['iso3','country','region','income_group']).to_dict(), 'vietnam_2023':vn.loc[2023].drop(labels=['iso3','country','region','income_group']).to_dict(), 'vietnam_working_age_peak_year':int(vn.age_15_64.idxmax()), 'vietnam_dependency_min_year':int(vn.total_dependency.idxmin()), 'vietnam_old_share_change_pp':float(vn.loc[2023,'age_65_plus']-vn.loc[1991,'age_65_plus']), 'vietnam_old_population_multiplier':float(vn.loc[2023,'population_65_plus']/vn.loc[1991,'population_65_plus']), 'vietnam_gdp_multiplier':float(vn.loc[2023,'gdp_ppp']/vn.loc[1991,'gdp_ppp']), 'sample_counts':{k:len(v) for k,v in samples.items()}, 'global_distribution':summaries, 'robustness':robust}
    threshold_summary = []
    for threshold in [8,10,12]:
        sub = crossings[(crossings.threshold.eq(threshold)) & crossings.status.eq('observed') & crossings.gdp_ppp.notna()]
        v = sub[sub.iso3.eq('VNM')]
        threshold_summary.append({'threshold':threshold,'n':len(sub),'median_gdp':sub.gdp_ppp.median(),'vietnam_year':int(v.year.iloc[0]) if len(v) else None,'vietnam_gdp':float(v.gdp_ppp.iloc[0]) if len(v) else None,'vietnam_percentile':float((sub.gdp_ppp<=v.gdp_ppp.iloc[0]).mean()*100) if len(v) else None})
    summary['benchmark_sensitivity'] = threshold_summary
    summary['demographic_insights'] = demographic_insights(df)
    write_json(out/'demographic_insights.json',summary['demographic_insights'])
    # Make threshold selection visible, including observed crossings excluded
    # solely because contemporaneous GDP is missing.
    funnel=crossings.assign(gdp_available=crossings.gdp_ppp.notna()).groupby(['threshold','status','gdp_available'],dropna=False).size().rename('economies').reset_index()
    funnel.to_csv(out/'threshold_sample_funnel.csv',index=False)
    end.reset_index().assign(in_gdp_sample=end.gdp_ppp.notna().to_numpy(),in_labor_sample=end.employment.notna().to_numpy()).groupby('region').agg(economies=('iso3','count'),gdp_sample=('in_gdp_sample','sum'),labor_sample=('in_labor_sample','sum')).to_csv(out/'sample_coverage_by_region.csv')
    write_json(out / 'analysis_summary.json', summary)
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return summary

if __name__ == '__main__': main()
