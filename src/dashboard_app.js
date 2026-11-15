'use strict';
const payload=JSON.parse(document.getElementById('data').textContent), M=AgingModel;
const rows=payload.rows, el=id=>document.getElementById(id), names=payload.names;
const countries=[...new Map(rows.map(r=>[r.iso3,names[r.iso3]||r.country])).entries()].sort((a,b)=>a[1].localeCompare(b[1]));
const labels=Object.fromEntries(countries), byCountry=new Map(countries.map(([c])=>[c,rows.filter(r=>r.iso3===c)]));
const n=(v,d=2)=>M.valid(v)?new Intl.NumberFormat('vi-VN',{maximumFractionDigits:d}).format(v):'Không có dữ liệu';
const sign=v=>M.valid(v)?(v>0?'+':'')+n(v):'Không có dữ liệu';
const pct=v=>M.valid(v)?n(v)+'%':'Không có dữ liệu';
const palette=['#39789b','#8b62a6','#009e73','#ad7d00','#5961a8','#ac5f7f'];
const color=c=>payload.colors[c]||palette[[...c].reduce((s,x)=>s+x.charCodeAt(0),0)%palette.length];
let view='overview',compare=['VNM','THA','IDN','JPN','KOR'],metric='age_65_plus',threshold=10,baseline='median',periodStart=2010,selectedSource='a',detailCode=null,sourcePage=0;
const sources={};
const fieldNames={iso3:'Mã',country:'Quốc gia',year:'Năm',region:'Vùng',population:'Dân số (người)',age_0_14:'0–14 (%)',age_15_64:'15–64 (%)',age_65_plus:'65+ (%)',population_65_plus:'65+ (người)',gdp_ppp:'GDP PPP/người',lfpr:'LFPR 15+ (%)',employment:'Có việc làm 15+ (%)',aging_index:'65+ /100 trẻ em',potential_support_ratio:'15–64 /1 người 65+',child_dependency:'Trẻ em /100 người 15–64',old_dependency:'65+ /100 người 15–64',total_dependency:'Phụ thuộc /100 người 15–64',annual_change_pp:'Thay đổi/năm (điểm %)',threshold:'Ngưỡng (%)',status:'Trạng thái'};
countries.forEach(([c,name])=>el('country').add(new Option(name,c)));el('country').value='VNM';
[...new Set(rows.map(r=>r.region.trim()))].sort().forEach(r=>el('region').add(new Option(r,r)));
el('hash').textContent='SHA256 master: '+payload.master_sha256;
function series(c,year){return byCountry.get(c).filter(r=>r.year<=year);}
function uniqueCodes(){return [...new Set([el('country').value,...compare])].slice(0,6);}
function chips(){
 el('chips').replaceChildren();compare=uniqueCodes();
 for(const code of compare){const b=document.createElement('button');b.className='chip';b.textContent=labels[code]+' ×';b.setAttribute('aria-label','Bỏ đối chiếu '+labels[code]);b.disabled=code===el('country').value;b.onclick=()=>{compare=compare.filter(c=>c!==code);render();};el('chips').append(b);}
 el('add-country').replaceChildren(new Option('Chọn quốc gia…',''));
 countries.filter(([c])=>!compare.includes(c)).forEach(([c,name])=>el('add-country').add(new Option(name,c)));
 el('add-country').disabled=compare.length>=6;
}
function kpis(items){
 el('kpis').replaceChildren();for(const [title,value,sub] of items){const card=document.createElement('div');card.className='kpi';for(const [tag,text] of [['span',title],['strong',value],['small',sub]]){const e=document.createElement(tag);e.textContent=text;card.append(e);}el('kpis').append(card);}
}
function options(label,id,values,current,handler){
 const l=document.createElement('label');l.append(document.createTextNode(label));const s=document.createElement('select');s.id=id;s.setAttribute('aria-label',label);values.forEach(([v,name])=>s.add(new Option(name,v)));s.value=current;s.onchange=()=>handler(s.value);l.append(s);el('extras').append(l);
}
function plot(slot,title,note,data,layout,sourceRows,columns,clickable=false){
 el('title-'+slot).textContent=title;el('note-'+slot).textContent=note;
 sources[slot]={title,note,rows:sourceRows,columns};
 const target=el('chart-'+slot);target.setAttribute('role','img');target.setAttribute('aria-label',title+'. '+note+'. Dữ liệu tương ứng nằm trong bảng bên dưới.');
 if(!data.some(t=>(t.orientation==='h'?(t.x||[]):(t.y||[])).some(M.valid)||(t.z||[]).flat().some(M.valid))){layout={...layout,annotations:[{text:'Không có dữ liệu cho phạm vi đã chọn',xref:'paper',yref:'paper',x:.5,y:.5,showarrow:false,font:{size:14,color:'#536577'}}]};}
 const base={font:{family:'Arial',size:12,color:'#172b3a'},margin:{t:20,l:65,r:20,b:65},paper_bgcolor:'white',plot_bgcolor:'white',legend:{orientation:'h',y:1.15},hovermode:'closest',autosize:true};
 Plotly.react(target,data,{...base,...layout},{responsive:true,displaylogo:false,displayModeBar:false}).then(()=>{
  target.removeAllListeners('plotly_click');
  if(clickable)target.on('plotly_click',e=>{const code=e.points[0]?.customdata;if(typeof code==='string'&&byCountry.has(code)){detailCode=code;detail();}});
 });
}
function line(c,s,key){return {x:s.map(r=>r.year),y:s.map(r=>r[key]),customdata:s.map(r=>r.iso3),name:labels[c],mode:s.length===1?'markers':'lines',connectgaps:false,line:{color:color(c),width:c===el('country').value?3:2},hovertemplate:labels[c]+'<br>Năm %{x}: %{y:,.2f}<extra></extra>'};}
function bars(sampleRows,key){return [{x:sampleRows.map(r=>r[key]),y:sampleRows.map(r=>labels[r.iso3]),customdata:sampleRows.map(r=>r.iso3),type:'bar',orientation:'h',marker:{color:sampleRows.map(r=>color(r.iso3))},hovertemplate:'%{y}<br>%{x:,.2f}<extra></extra>'}];}
function crossData(s,x,y){return [{x:s.map(r=>r[x]),y:s.map(r=>r[y]),customdata:s.map(r=>r.iso3),text:s.map(r=>labels[r.iso3]),type:'scatter',mode:'markers',marker:{color:s.map(r=>compare.includes(r.iso3)?color(r.iso3):'#b0bfcb'),size:s.map(r=>compare.includes(r.iso3)?11:7),symbol:s.map(r=>r.iso3===el('country').value?'diamond':'circle')},hovertemplate:'%{text}<br>x: %{x:,.2f}<br>y: %{y:.2f}<extra></extra>'}];}
function source(slot=selectedSource,keepPage=false){
 if(!keepPage||slot!==selectedSource)sourcePage=0;selectedSource=slot;const s=sources[slot];el('source-title').textContent='Dữ liệu · '+s.title;
 const page=M.page(s.rows,sourcePage);sourcePage=page.index;
 el('source-caption').textContent=s.note+' '+s.rows.length+' dòng; CSV chứa toàn bộ phạm vi biểu đồ. Snapshot '+payload.snapshot+'.';
 el('source-page').textContent='Trang '+(page.index+1)+' / '+page.count+' · '+page.total+' dòng';el('source-prev').disabled=page.index===0;el('source-next').disabled=page.index+1===page.count;
 el('source-head').replaceChildren();el('source-body').replaceChildren();const tr=document.createElement('tr');
 for(const c of s.columns){const th=document.createElement('th');th.scope='col';th.textContent=fieldNames[c]||c;tr.append(th);}el('source-head').append(tr);
 for(const r of page.rows){const tr=document.createElement('tr');for(const c of s.columns){const td=document.createElement('td');td.textContent=c==='year'?String(r[c]??'—'):typeof r[c]==='number'?n(r[c],3):(r[c]??'—');tr.append(td);}el('source-body').append(tr);}
}
function download(slot){
 const s=sources[slot],blob=new Blob([M.csv(s.rows,s.columns)],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');
 a.href=url;a.download='aging-'+view+'-'+slot+'-'+el('year').value+'.csv';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);
 el('status').textContent='Đã yêu cầu tải CSV: '+s.rows.length+' dòng · '+s.title+'.';
}
function detail(){
 if(!detailCode)return;const s=series(detailCode,+el('year').value);el('detail').hidden=false;el('detail-title').textContent=labels[detailCode]+' · tỷ trọng 65+';
 Plotly.react(el('detail-chart'),[line(detailCode,s,'age_65_plus')],{margin:{t:20,l:55,r:20,b:45},xaxis:{title:{text:'Năm'}},yaxis:{title:{text:'% tổng dân số'}},showlegend:false,font:{family:'Arial'}},{responsive:true,displayModeBar:false});
 el('detail').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'nearest'});
}
function render(){
 const year=+el('year').value,code=el('country').value,region=el('region').value,focus=series(code,year),current=focus.find(r=>r.year===year),first=focus.find(r=>r.year===1991),selected=uniqueCodes();
 const slice=M.sample(rows,year,region),history=selected.flatMap(c=>series(c,year));
 el('yearText').value=year;el('year').setAttribute('aria-valuetext',String(year));chips();el('extras').replaceChildren();el('status').textContent='';
 el('card-d').hidden=view!=='aging';
 el('dashboard').setAttribute('aria-labelledby','tab-'+view);
 el('scope').textContent=labels[code]+' · năm '+year+'. Lịch sử quốc gia: 1991–'+year+'. Vùng so sánh chỉ áp dụng mẫu lát cắt, tốc độ vùng và mốc già hóa; không loại quốc gia đã chọn khỏi chuỗi lịch sử.';
 const common=['iso3','country','year'];
 const oldChange=M.change(first,current,'age_65_plus');
 if(view==='overview'){
  kpis([['Dân số',n(M.scaled(current.population,1e6))+' triệu','Năm '+year],['Dân số 65+',pct(current.age_65_plus),sign(oldChange)+' điểm % so với 1991'],['Số người 65+',n(M.scaled(current.population_65_plus,1e6))+' triệu','Ước tính từ dân số × tỷ trọng 65+'],['Tỷ lệ phụ thuộc',n(current.total_dependency),'Trên 100 người 15–64; '+sign(M.change(first,current,'total_dependency'))+' so với 1991']]);
  const bm=M.benchmark(slice,'age_65_plus');
  el('finding').textContent=labels[code]+' có '+n(current.age_65_plus)+'% dân số 65+; trung vị '+n(bm.median)+'% của '+bm.n+'/'+bm.total+' nền kinh tế trong vùng so sánh năm '+year+'. Mức tổng hợp theo dân số trên cùng mẫu là '+n(bm.weighted)+'%.';
  const ageKeys=['age_0_14','age_15_64','age_65_plus'],ageColors=['#6aaf9d','#39789b','#c54b27'];
  plot('a','Cơ cấu tuổi · '+labels[code],'Tỷ trọng trong tổng dân số · 1991–'+year,ageKeys.map((key,i)=>({x:focus.map(r=>r.year),y:focus.map(r=>r[key]),name:['0–14','15–64','65+'][i],type:'scatter',mode:'lines',stackgroup:'age',connectgaps:false,line:{color:ageColors[i]},hovertemplate:'Năm %{x}: %{y:.2f}%<extra></extra>'})),{yaxis:{range:[0,100],ticksuffix:'%'}},focus,[...common,...ageKeys]);
  plot('b','Đối chiếu tỷ trọng 65+','Các quốc gia đã chọn · 1991–'+year,selected.map(c=>line(c,series(c,year),'age_65_plus')),{yaxis:{ticksuffix:'%',rangemode:'tozero'}},history,[...common,'age_65_plus']);
  const top=slice.filter(r=>M.valid(r.age_65_plus)).sort((a,b)=>b.age_65_plus-a.age_65_plus).slice(0,15).reverse();
  plot('c','Tỷ trọng 65+ cao trong vùng so sánh','15 nền kinh tế cao nhất · năm '+year+' · bấm cột để xem lịch sử',bars(top,'age_65_plus'),{margin:{t:10,l:140,r:15,b:45},xaxis:{ticksuffix:'%'},yaxis:{automargin:true}},top,[...common,'region','age_65_plus'],true);
 }else if(view==='aging'){
  options('Đại lượng theo dõi','metric',[['age_65_plus','Tỷ trọng 65+ (%)'],['population_65_plus','Số người 65+'],['aging_index','Người 65+ /100 trẻ em']],metric,v=>{metric=v;render();});
  options('Đường so sánh tỷ trọng 65+','baseline',[['median','Trung vị các nền kinh tế'],['weighted','Tổng hợp theo dân số']],baseline,v=>{baseline=v;render();});
  el('baseline').disabled=metric!=='age_65_plus';
  options('Năm đầu tính tốc độ','period-start',[[1991,'1991'],[2000,'2000'],[2010,'2010']],String(periodStart),v=>{periodStart=+v;render();});
  kpis([['Chỉ số già hóa',n(current.aging_index),'Người 65+ trên 100 trẻ em'],['Hỗ trợ tiềm năng',n(current.potential_support_ratio),'Người 15–64 trên một người 65+'],['Phụ thuộc tuổi già',n(current.old_dependency),'Người 65+ trên 100 người 15–64'],['Thay đổi 65+',sign(oldChange)+' điểm %','So với 1991; không phải tốc độ năm']]);
  const trough=focus.reduce((a,b)=>b.total_dependency<a.total_dependency?b:a,focus[0]);
  el('finding').textContent='Trong 1991–'+year+', '+labels[code]+' có tỷ lệ phụ thuộc thấp nhất quan sát năm '+trough.year+' ('+n(trough.total_dependency)+'). Đến '+year+' thay đổi '+sign(current.total_dependency-trough.total_dependency)+' trên 100 người 15–64. Đây là diễn biến nhân khẩu học, không xác định tác động kinh tế.';
  const data=selected.map(c=>line(c,series(c,year),metric));let sourceRows=history,cols=[...common,metric];
  if(metric==='age_65_plus'){
   const benchmarks=[];for(let y=1991;y<=year;y++){const b=M.benchmark(M.sample(rows,y,region),'age_65_plus');benchmarks.push({year:y,value:b[baseline],sample_n:b.n});}
   data.push({x:benchmarks.map(r=>r.year),y:benchmarks.map(r=>r.value),name:baseline==='median'?'Trung vị vùng':'Tổng hợp theo dân số',mode:'lines',line:{color:'#6b7785',dash:'dash'},connectgaps:false});
   sourceRows=[...history.map(r=>({...r,series_kind:'country'})),...benchmarks.map(r=>({country:'Benchmark vùng',year:r.year,age_65_plus:r.value,series_kind:baseline,region,sample_n:r.sample_n}))];cols=[...common,metric,'series_kind','region','sample_n'];
  }
  plot('a','Diễn biến · '+fieldNames[metric],'Chuỗi quốc gia đã chọn; benchmark chỉ áp dụng tỷ trọng 65+. Mẫu benchmark có thể thay đổi theo năm.',data,{yaxis:{title:{text:fieldNames[metric]},rangemode:'tozero'}},sourceRows,cols);
  const start=periodStart,duration=year-start;
  const rates=duration>0?slice.map(r=>{const a=byCountry.get(r.iso3).find(x=>x.year===start),change=M.change(a,r,'age_65_plus');return {...r,start_year:start,annual_change_pp:M.valid(change)?change/duration:null};}).filter(r=>M.valid(r.annual_change_pp)).sort((a,b)=>b.annual_change_pp-a.annual_change_pp).slice(0,15).reverse():[];
  plot('b','Tốc độ tăng tỷ trọng 65+',duration>0?'15 mức tăng/năm cao nhất trong vùng · '+start+'–'+year:'Chưa tính tốc độ: chọn năm kết thúc sau '+start,bars(rates,'annual_change_pp'),{margin:{t:10,l:135,r:15,b:45},xaxis:{title:{text:'Điểm phần trăm mỗi năm'}},yaxis:{automargin:true}},rates,[...common,'start_year','annual_change_pp'],true);
  plot('c','Thành phần phụ thuộc · '+labels[code],'Trẻ em và tuổi già trên 100 người 15–64', ['child_dependency','old_dependency'].map((key,i)=>({x:focus.map(r=>r.year),y:focus.map(r=>r[key]),name:i?'Tuổi già':'Trẻ em',mode:'lines',stackgroup:'dependency',connectgaps:false,line:{color:i?'#c54b27':'#39789b'}})),{yaxis:{rangemode:'tozero'}},focus,[...common,'child_dependency','old_dependency','total_dependency']);
  const heatRows=history.map(r=>{const prev=byCountry.get(r.iso3).find(x=>x.year===r.year-1);return {...r,annual_change_pp:M.change(prev,r,'age_65_plus')};});
  plot('d','Thay đổi già hóa qua từng năm','Quốc gia đã chọn · thay đổi tỷ trọng 65+ so với năm trước, điểm %; 1991 không có năm gốc trong cửa sổ.',[{type:'heatmap',x:focus.map(r=>r.year),y:selected.map(c=>labels[c]),z:selected.map(c=>heatRows.filter(r=>r.iso3===c).map(r=>r.annual_change_pp)),colorscale:'RdBu',reversescale:true,zmid:0,colorbar:{title:{text:'Điểm %'}},hoverongaps:false,hovertemplate:'%{y} · %{x}<br>Thay đổi %{z:.3f} điểm %<extra></extra>'}],{margin:{t:15,l:105,r:65,b:45}},heatRows,[...common,'age_65_plus','annual_change_pp']);
 }else if(view==='economy'){
  options('Mốc tỷ trọng 65+','threshold',[[8,'8%'],[10,'10%'],[12,'12%']],String(threshold),v=>{threshold=+v;render();});
  const sample=M.pair(slice,'gdp_ppp','age_65_plus').filter(r=>r.gdp_ppp>0),corr=M.correlation(sample,'gdp_ppp','age_65_plus',true);
  const codes=new Set(M.sample(rows,2023,region).map(r=>r.iso3)),t=M.thresholdSample(payload.crossings,threshold,codes),eligible=t.eligible.sort((a,b)=>a.gdp_ppp-b.gdp_ppp),vn=t.all.find(r=>r.iso3===code);
  kpis([['GDP/người PPP',n(current.gdp_ppp),'Đô la quốc tế, giá '+payload.price_base],['Tỷ trọng 65+',pct(current.age_65_plus),'Quốc gia trọng tâm · '+year],['Mẫu GDP–già hóa',sample.length+'/'+slice.length,'Nền kinh tế đủ hai biến · '+year],['Tương quan Pearson',n(corr),'log GDP/người với tỷ trọng 65+']]);
  el('finding').textContent='Tương quan mô tả năm '+year+' là '+n(corr)+' trên '+sample.length+' nền kinh tế. Tại mốc '+threshold+'%, '+labels[code]+': '+(vn?.status==='observed'?'lần vượt quan sát năm '+vn.year:vn?.status==='already_above'?'đã ở trên mốc khi bắt đầu cửa sổ':'chưa có lần vượt đủ điều kiện trong 1991–2023')+'. Không xác định quan hệ nhân quả hoặc tiêu chuẩn “giàu”.';
  plot('a','Thu nhập và tỷ trọng 65+','Năm '+year+' · n='+sample.length+'/'+slice.length+' · trục GDP log · bấm điểm để xem lịch sử',crossData(sample,'gdp_ppp','age_65_plus'),{xaxis:{type:'log',title:{text:'GDP PPP/người, giá '+payload.price_base}},yaxis:{title:{text:'65+ (% tổng dân số)'}}},sample,[...common,'gdp_ppp','age_65_plus'],true);
  plot('b','Quỹ đạo thu nhập–già hóa','Quốc gia đã chọn · 1991–'+year+' · GDP giá cố định; không nối qua thiếu',selected.map(c=>{const s=series(c,year);return {x:s.map(r=>r.gdp_ppp),y:s.map(r=>r.age_65_plus),text:s.map(r=>r.year),name:labels[c],mode:'lines+markers',connectgaps:false,line:{color:color(c)},marker:{size:4},hovertemplate:labels[c]+' · %{text}<br>GDP: %{x:,.0f}<br>65+: %{y:.2f}%<extra></extra>'};}),{xaxis:{type:'log',title:{text:'GDP PPP/người'}},yaxis:{title:{text:'65+ (%)'}}},history,[...common,'gdp_ppp','age_65_plus']);
  const counts=t.counts,missing=(counts.observed||0)-eligible.length;
  plot('c','Thu nhập tại lần vượt '+threshold+'%','Cửa sổ cố định 1991–2023; không theo bộ lọc năm. '+t.all.length+' nền kinh tế → '+(counts.observed||0)+' vượt quan sát → '+eligible.length+' có GDP; '+(counts.already_above||0)+' đã trên mốc, '+(counts.not_reached||0)+' chưa đạt, '+missing+' vượt nhưng thiếu GDP; '+(counts.gap_uncertain||0)+' không chắc do thiếu.',[{x:eligible.map(r=>r.gdp_ppp),y:eligible.map((r,i)=>i+1),text:eligible.map(r=>labels[r.iso3]+' · '+r.year),customdata:eligible.map(r=>r.iso3),mode:'markers',marker:{color:eligible.map(r=>color(r.iso3)),size:7},hovertemplate:'%{text}<br>GDP PPP/người: %{x:,.0f}<extra></extra>'}],{xaxis:{type:'log',title:{text:'GDP PPP/người tại mốc'}},yaxis:{title:{text:'Thứ tự trong mẫu'}}},eligible,['iso3','country','threshold','year','gdp_ppp','status'],true);
 }else{
  const sample=M.pair(slice,'age_15_64','employment'),corr=M.correlation(sample,'age_15_64','employment');
  const base2019=byCountry.get(code).find(r=>r.year===2019),start=year>=2019?2019:1991,ref=year>=2019?base2019:first;
  kpis([['Dân số 15–64',pct(current.age_15_64),'Mẫu số tổng dân số'],['Lực lượng lao động',pct(current.lfpr),'Mẫu số dân số 15+ · ILO mô hình'],['Có việc làm',pct(current.employment),'Mẫu số dân số 15+ · ILO mô hình'],['Tương quan lát cắt',n(corr),'n='+sample.length+'/'+slice.length+' · năm '+year]]);
  el('finding').textContent=labels[code]+' · '+start+'–'+year+': LFPR thay đổi '+sign(M.change(ref,current,'lfpr'))+' điểm %, tỷ lệ có việc làm '+sign(M.change(ref,current,'employment'))+' điểm %. Các tỷ lệ lao động và tỷ trọng tuổi có mẫu số khác nhau; không cộng hoặc coi biến động là tác động của già hóa.';
  plot('a','Cơ cấu tuổi và việc làm trong cùng năm','Năm '+year+' · n='+sample.length+'/'+slice.length+' · bấm điểm để xem lịch sử',crossData(sample,'age_15_64','employment'),{xaxis:{title:{text:'15–64 / tổng dân số (%)'}},yaxis:{title:{text:'Có việc làm / dân số 15+ (%)'}}},sample,[...common,'age_15_64','employment'],true);
  plot('b','Hai tỷ lệ lao động · '+labels[code],'1991–'+year+' · cùng mẫu số dân số 15+; giữ khoảng thiếu', ['lfpr','employment'].map((key,i)=>({...line(code,focus,key),name:i?'Có việc làm':'Lực lượng lao động',line:{color:i?'#39789b':'#c54b27'}})),{yaxis:{ticksuffix:'%',range:[0,100]}},focus,[...common,'lfpr','employment']);
  plot('c','Tỷ trọng 15–64 · đối chiếu quốc gia','1991–'+year+' · tỷ trọng trong tổng dân số',selected.map(c=>line(c,series(c,year),'age_15_64')),{yaxis:{ticksuffix:'%',range:[0,100]}},history,[...common,'age_15_64']);
 }
 source();if(detailCode)detail();
}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{view=b.dataset.view;document.querySelectorAll('[data-view]').forEach(x=>{x.setAttribute('aria-selected',String(x===b));x.tabIndex=x===b?0:-1;});selectedSource='a';detailCode=null;el('detail').hidden=true;render();});
document.querySelectorAll('[data-source]').forEach(b=>b.onclick=()=>{source(b.dataset.source);el('source-title').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});});
document.querySelectorAll('[data-export]').forEach(b=>b.onclick=()=>download(b.dataset.export));
['year','region','country'].forEach(id=>el(id).addEventListener(id==='year'?'input':'change',render));
el('add-country').onchange=()=>{if(el('add-country').value&&compare.length<6)compare.push(el('add-country').value);render();};
el('reset').onclick=()=>{el('country').value='VNM';el('year').value='2023';el('region').value='All';compare=['VNM','THA','IDN','JPN','KOR'];metric='age_65_plus';threshold=10;baseline='median';periodStart=2010;detailCode=null;el('detail').hidden=true;render();};
el('close-detail').onclick=()=>{detailCode=null;el('detail').hidden=true;};
render();

const tabs=[...document.querySelectorAll('[data-view]')];
tabs.forEach((tab,index)=>tab.addEventListener('keydown',event=>{let next;if(event.key==='ArrowRight')next=(index+1)%tabs.length;else if(event.key==='ArrowLeft')next=(index+tabs.length-1)%tabs.length;else if(event.key==='Home')next=0;else if(event.key==='End')next=tabs.length-1;else return;event.preventDefault();tabs[next].focus();tabs[next].click();}));
el('source-prev').onclick=()=>{sourcePage--;source(selectedSource,true);};
el('source-next').onclick=()=>{sourcePage++;source(selectedSource,true);};
