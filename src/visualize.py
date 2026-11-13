"""Twelve reproducible principal figures, with matching CSV inputs and SVG exports."""
import io
import json
import zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from matplotlib.ticker import FuncFormatter, FixedLocator, NullFormatter
import shapefile
from config import ROOT, FOCAL, COLORS, YEARS

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.titlesize':14,'axes.labelsize':11,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.2,'axes.axisbelow':True,'svg.fonttype':'none','savefig.facecolor':'white'})
FIG = ROOT / 'outputs/figures'
TABLE = ROOT / 'outputs/tables'
BASE = json.loads((ROOT / 'data/metadata/price_base.json').read_text())['year'] if (ROOT / 'data/metadata/price_base.json').exists() else None

def save(fig, number, slug, title, sample, data):
    fig.suptitle(f'Hình {number:02d}. {title}', x=.04, ha='left', fontsize=16, fontweight='bold')
    fig.text(.04,.022,f'Nguồn: World Bank WDI; tính toán của dự án. {sample}',fontsize=9,color='#4b5563')
    fig.tight_layout(rect=[.02,.065,.98,.93],pad=1.5)
    name=f'{number:02d}_{slug}'
    fig.savefig(FIG/(name+'.png'),dpi=190)
    fig.savefig(FIG/(name+'.svg'))
    data.to_csv(TABLE/(f'figure_{number:02d}_data.csv'),index=False)
    plt.close(fig)
    return name

def time_axis(ax):
    ax.set_xlim(1991,2023)
    ax.set_xticks([1991,2000,2010,2023])
    ax.set_xlabel('Năm')

def main():
    df=pd.read_csv(ROOT/'data/processed/master.csv')
    vn=df[df.iso3.eq('VNM')].set_index('year').reindex(YEARS)
    focal=df[df.iso3.isin(FOCAL)]
    names=[]
    fig,ax=plt.subplots(figsize=(10.5,6))
    ax.stackplot(vn.index,vn.age_0_14,vn.age_15_64,vn.age_65_plus,labels=['0–14 tuổi','15–64 tuổi','65 tuổi trở lên'],colors=['#B9CEDC','#39789B','#C54B27'])
    ax.set_ylim(0,100); ax.set_ylabel('Tỷ trọng trong tổng dân số (%)'); time_axis(ax)
    ax.legend(loc='lower left',ncol=3,framealpha=.95)
    names.append(save(fig,1,'age_structure','Cơ cấu tuổi của Việt Nam, 1991–2023','Việt Nam, 33 năm.',vn.reset_index()))
    fig,axs=plt.subplots(1,2,figsize=(10.5,5.5))
    for ax,col,unit,scale in zip(axs,['population_65_plus','age_65_plus'],['Triệu người từ 65 tuổi','Tỷ trọng 65+ (%)'],[1e6,1]):
        ax.plot(vn.index,vn[col]/scale,color=COLORS['VNM'],lw=2.5)
        ax.scatter([1991,2023],vn.loc[[1991,2023],col]/scale,color=COLORS['VNM'])
        for yr in [1991,2023]:ax.annotate(f'{vn.loc[yr,col]/scale:.2f}',(yr,vn.loc[yr,col]/scale),xytext=(8 if yr==1991 else -35,10),textcoords='offset points')
        ax.set_ylabel(unit); ax.set_ylim(bottom=0);time_axis(ax)
    names.append(save(fig,2,'older_population','Quy mô và tỷ trọng dân số cao tuổi','Việt Nam, 1991–2023; số người 65+ là biến dẫn xuất.',vn.reset_index()))
    fig,ax=plt.subplots(figsize=(10.5,5.8))
    for col,label,color,style in [('child_dependency','Phụ thuộc trẻ em','#39789B','--'),('old_dependency','Phụ thuộc tuổi già','#C54B27','-'),('total_dependency','Phụ thuộc tổng cộng','#333333','-.')]:
        ax.plot(vn.index,vn[col],label=label,color=color,lw=2.4,ls=style)
    ax.set_ylabel('Số người / 100 người 15–64 tuổi');ax.set_ylim(bottom=0);time_axis(ax);ax.legend(frameon=False)
    trough=int(vn.total_dependency.idxmin())
    ax.scatter([trough],[vn.loc[trough,'total_dependency']],color='#333333',zorder=4)
    ax.annotate(f'Đáy quan sát {trough}: {vn.loc[trough,"total_dependency"]:.2f}',(trough,vn.loc[trough,'total_dependency']),xytext=(-100,-38),textcoords='offset points',arrowprops={'arrowstyle':'->','color':'#555555'},fontsize=10)
    names.append(save(fig,3,'dependency','Các thành phần phụ thuộc nhân khẩu học','Việt Nam, 1991–2023. Không phải phụ thuộc tài chính.',vn.reset_index()))
    # Natural Earth geometry. ISO_A3_EH repairs -99 ISO_A3 cases where available.
    with zipfile.ZipFile(ROOT/'data/raw/natural_earth_countries.zip') as z:
        stem='ne_110m_admin_0_countries'
        reader=shapefile.Reader(shp=io.BytesIO(z.read(stem+'.shp')),shx=io.BytesIO(z.read(stem+'.shx')),dbf=io.BytesIO(z.read(stem+'.dbf')),encoding='utf-8')
        shapes=list(reader.iterShapeRecords())
    cross=df[df.year.eq(2023)].set_index('iso3')
    patches,values,matches=[],[],[]
    geometry_codes=set()
    for sr in shapes:
        record=sr.record.as_dict()
        code=record.get('ISO_A3_EH',record['ADM0_A3'])
        if code == '-99':code=record['ADM0_A3']
        if code=='KOS':code='XKX'
        if code=='ATA':continue
        geometry_codes.add(code)
        value=cross.loc[code,'age_65_plus'] if code in cross.index else np.nan
        matches.append({'geometry_name':record['NAME'],'mapped_iso3':code,'matched':code in cross.index,'has_value':bool(pd.notna(value))})
        points=np.array(sr.shape.points)
        bounds=list(sr.shape.parts)+[len(points)]
        for a,b in zip(bounds[:-1],bounds[1:]):
            patches.append(Polygon(points[a:b],closed=True));values.append(value)
    pd.DataFrame(matches).to_csv(TABLE/'map_geometry_matches.csv',index=False)
    cross.loc[~cross.index.isin(geometry_codes)].reset_index().to_csv(TABLE/'map_data_without_geometry.csv',index=False)
    fig,ax=plt.subplots(figsize=(11.5,6.3))
    cmap=plt.get_cmap('YlOrBr').copy();cmap.set_bad('#D6D6D6')
    pc=PatchCollection(patches,cmap=cmap,norm=Normalize(0,35),edgecolor='white',linewidth=.25)
    pc.set_array(np.ma.masked_invalid(values));ax.add_collection(pc);ax.set_xlim(-180,180);ax.set_ylim(-58,85);ax.set_aspect('equal');ax.axis('off')
    cb=fig.colorbar(pc,ax=ax,orientation='horizontal',fraction=.045,pad=.02);cb.set_label('Dân số 65+ (% tổng dân số)')
    ax.legend(handles=[Patch(facecolor='#D6D6D6',label='Thiếu dữ liệu / ngoài mẫu')],loc='lower left',frameon=False)
    names.append(save(fig,4,'world_map','Phân bố già hóa dân số năm 2023',f'n={cross.age_65_plus.notna().sum()} nền kinh tế; hình học Natural Earth 1:110m.',cross.reset_index()))
    ep=pd.read_csv(TABLE/'endpoints.csv'); five=ep[ep.iso3.isin(FOCAL)].sort_values('age_65_plus_2023')
    fig,axs=plt.subplots(1,2,figsize=(11,6),gridspec_kw={'width_ratios':[1.3,1]})
    ax=axs[0]
    for y,(_,r) in enumerate(five.iterrows()):
        ax.plot([r.age_65_plus_1991,r.age_65_plus_2023],[y,y],color=COLORS[r.iso3],lw=2)
        ax.scatter(r.age_65_plus_1991,y,facecolor='white',edgecolor=COLORS[r.iso3],s=65,zorder=3)
        ax.scatter(r.age_65_plus_2023,y,color=COLORS[r.iso3],s=65,zorder=3)
        ax.annotate(f'+{r.aging_change_pp:.1f} đpt',(r.age_65_plus_2023,y),xytext=(8,0),textcoords='offset points',va='center',fontsize=10)
    ax.set_yticks(range(len(five)),[FOCAL[c] for c in five.iso3]);ax.set_xlim(0,36);ax.set_xlabel('Tỷ trọng 65+ (%)');ax.set_title('Rỗng: 1991; đặc: 2023')
    valid=ep.dropna(subset=['aging_change_pp'])
    axs[1].hist(valid.aging_change_pp,bins=18,color='#9BB9CD',edgecolor='white')
    delta=float(five[five.iso3.eq('VNM')].aging_change_pp.iloc[0]);axs[1].axvline(delta,color=COLORS['VNM'],lw=2,label=f'Việt Nam: {delta:.1f} đpt');axs[1].legend(frameon=False)
    axs[1].set_xlabel('Thay đổi tỷ trọng 65+ (điểm phần trăm)');axs[1].set_ylabel('Số nền kinh tế');axs[1].set_title(f'Phân bố toàn cầu (n={len(valid)})')
    names.append(save(fig,5,'endpoint_change','Mức già hóa và thay đổi, 1991–2023','Mẫu đầu–cuối cố định; phân bố không trọng số.',ep))
    periods=pd.read_csv(TABLE/'period_changes.csv')
    pivot=periods.pivot(index='iso3',columns='period',values='annual_change_pp')
    # Focal countries + evenly spaced positions in endpoint aging-change distribution.
    ordered=valid.sort_values('aging_change_pp').iso3.tolist()
    codes=list(dict.fromkeys(list(FOCAL)+[ordered[i] for i in np.linspace(0,len(ordered)-1,22).astype(int)]))
    heat=pivot.reindex(codes).sort_values('2010–2023',ascending=False)
    fig,ax=plt.subplots(figsize=(10,9))
    im=ax.imshow(heat.values,cmap='RdBu_r',vmin=-.65,vmax=.65,aspect='auto')
    ax.set_yticks(range(len(heat)),[FOCAL.get(c,c) for c in heat.index]);ax.set_xticks(range(3),heat.columns);ax.grid(False)
    for i in range(len(heat)):
        for j in range(3):
            value=heat.iloc[i,j]
            ax.text(j,i,'—' if pd.isna(value) else f'{value:.2f}',ha='center',va='center',fontsize=9,color='white' if abs(value)>.38 else '#222222')
    fig.colorbar(im,ax=ax,label='Điểm phần trăm mỗi năm',fraction=.05)
    names.append(save(fig,6,'aging_heatmap','Tốc độ già hóa qua các giai đoạn',f'{len(heat)} nền kinh tế: 5 trọng tâm + 22 vị trí trải đều trong phân bố thay đổi.',periods[periods.iso3.isin(heat.index)]))
    fig,axs=plt.subplots(1,5,figsize=(13,4.8),sharey=True)
    for ax,(code,label) in zip(axs,FOCAL.items()):
        g=focal[focal.iso3.eq(code)].set_index('year').reindex(YEARS)
        ax.plot(g.index,g.fertility,color=COLORS[code],lw=2);ax.set_title(label);time_axis(ax);ax.set_xticks([1991,2023]);ax.set_ylim(0,5)
        ax.annotate(f'{g.loc[2023,"fertility"]:.2f}',(2023,g.loc[2023,'fertility']),xytext=(-30,12),textcoords='offset points')
    axs[0].set_ylabel('Số con / phụ nữ')
    names.append(save(fig,7,'fertility','Mức sinh của năm nền kinh tế trọng tâm','1991–2023. Mức sinh là bối cảnh dài hạn, không phải tác động tức thời lên nhóm 65+.',focal))
    scat=pd.read_csv(TABLE/'gdp_aging_2023.csv')
    fig,ax=plt.subplots(figsize=(10.5,6.3))
    ax.scatter(scat.gdp_ppp,scat.age_65_plus,s=28,color='#8EABC0',alpha=.65,edgecolor='white',lw=.3)
    for code,label in FOCAL.items():
        r=scat[scat.iso3.eq(code)].iloc[0];ax.scatter(r.gdp_ppp,r.age_65_plus,color=COLORS[code],s=65,zorder=3)
        ax.annotate(label,(r.gdp_ppp,r.age_65_plus),xytext=(7,6),textcoords='offset points',fontsize=10)
    ax.set_xscale('log');ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:,.0f}'));ax.set_xlabel(f'GDP/người PPP (đô la quốc tế giá {BASE}; trục log)');ax.set_ylabel('Tỷ trọng dân số 65+ (%)')
    names.append(save(fig,8,'gdp_aging','Thu nhập và già hóa trong cùng năm 2023',f'n={len(scat)} nền kinh tế, mỗi điểm có trọng số như nhau.',scat))
    fig,ax=plt.subplots(figsize=(10.5,6.5))
    for code,label in FOCAL.items():
        g=focal[focal.iso3.eq(code)].set_index('year').reindex(YEARS)
        ax.plot(g.gdp_ppp,g.age_65_plus,color=COLORS[code],lw=2,label=label)
        for yr,marker in [(1991,'o'),(2010,'s'),(2023,'^')]:
            ax.scatter(g.loc[yr,'gdp_ppp'],g.loc[yr,'age_65_plus'],color=COLORS[code],marker=marker,s=55)
        ax.annotate(label,(g.loc[2023,'gdp_ppp'],g.loc[2023,'age_65_plus']),xytext=(6,3),textcoords='offset points',fontsize=10)
    ax.axhline(10,color='#777777',ls='--',lw=1);ax.set_xscale('log');ax.set_xlim(1500,85000);ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:,.0f}'));ax.set_xlabel(f'GDP/người PPP (đô la quốc tế giá {BASE}; trục log)');ax.set_ylabel('Dân số 65+ (%)')
    ax.xaxis.set_major_locator(FixedLocator([2000,5000,10000,20000,50000]))
    ax.xaxis.set_minor_formatter(NullFormatter())
    names.append(save(fig,9,'trajectories','Quỹ đạo thu nhập và già hóa, 1991–2023','Tròn: 1991; vuông: 2010; tam giác: 2023. Đường ngang: mốc phân tích 10%.',focal))
    crossings=pd.read_csv(TABLE/'threshold_crossings.csv')
    bench=crossings[crossings.threshold.eq(10)&crossings.status.eq('observed')&crossings.gdp_ppp.notna()].sort_values('gdp_ppp')
    fig,ax=plt.subplots(figsize=(10.5,8.5))
    # Show all valid global crossings, country identifiers compact and exact values in CSV.
    ax.scatter(bench.gdp_ppp,range(len(bench)),c=[COLORS.get(c,'#8EABC0') for c in bench.iso3],s=35)
    labels=[f'{FOCAL.get(r.iso3,r.iso3)} ({int(r.year)})' for r in bench.itertuples()]
    ax.set_yticks(range(len(bench)),labels,fontsize=8);ax.set_xscale('log');ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:,.0f}'));ax.set_xlabel(f'GDP/người PPP tại năm vượt ngưỡng (giá {BASE}; trục log)');ax.grid(axis='y',alpha=.15)
    names.append(save(fig,10,'aging_benchmark','Thu nhập khi lần đầu quan sát vượt mốc 10%',f'n={len(bench)}; 1991–2023; loại trường hợp đã vượt từ đầu, thiếu năm hoặc thiếu GDP.',bench))
    fig,axs=plt.subplots(3,1,figsize=(10.5,8),sharex=True)
    for ax,col,title in zip(axs,['age_15_64','lfpr','employment'],['Dân số 15–64 / tổng dân số (%)','Lực lượng lao động / dân số 15+ (%)','Người có việc làm / dân số 15+ (%)']):
        ax.plot(vn.index,vn[col],color=COLORS['VNM'],lw=2.3);ax.set_title(title,loc='left',fontsize=12);ax.set_ylim(45,85);time_axis(ax)
    names.append(save(fig,11,'vietnam_labor','Cơ cấu tuổi và các tỷ lệ lao động ở Việt Nam','1991–2023. Hai chỉ tiêu lao động: ILO mô hình; mẫu số khác tỷ trọng 15–64.',vn.reset_index()))
    labor=pd.read_csv(TABLE/'labor_2023.csv')
    fig,ax=plt.subplots(figsize=(10.5,6.3))
    ax.scatter(labor.age_15_64,labor.employment,color='#8EABC0',s=30,alpha=.65)
    for code,label in FOCAL.items():
        r=labor[labor.iso3.eq(code)].iloc[0];ax.scatter(r.age_15_64,r.employment,color=COLORS[code],s=65)
        ax.annotate(label,(r.age_15_64,r.employment),xytext=(7,6),textcoords='offset points',fontsize=10)
    ax.set_xlabel('Dân số 15–64 / tổng dân số (%)');ax.set_ylabel('Người có việc làm / dân số 15+ (%)')
    names.append(save(fig,12,'labor_scatter','Cơ cấu tuổi và tỷ lệ có việc làm năm 2023',f'n={len(labor)}. ILO mô hình: thăm dò mô tả, không dùng để xếp hạng hiệu quả quốc gia.',labor))
    (FIG/'figure_index.json').write_text(json.dumps(names,indent=2),'utf-8')
    # Supplementary distribution chart preserves the balanced country sample.
    print(f'Exported {len(names)} principal figures (PNG + SVG)')
    return names

if __name__=='__main__':main()
