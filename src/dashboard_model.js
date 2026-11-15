/* Pure calculations shared by browser and Node verification. */
(function(root){
 'use strict';
 const valid=v=>typeof v==='number'&&Number.isFinite(v);
 const median=a=>{const b=a.filter(valid).sort((x,y)=>x-y),n=b.length;return n?(b[Math.floor(n/2)]+b[Math.ceil(n/2)-1])/2:null;};
 const pair=(rows,x,y)=>rows.filter(r=>valid(r[x])&&valid(r[y]));
 function correlation(rows,x,y,logX=false){
  const p=pair(rows,x,y).filter(r=>!logX||r[x]>0);if(p.length<3)return null;
  const a=p.map(r=>logX?Math.log(r[x]):r[x]),b=p.map(r=>r[y]);
  const ma=a.reduce((s,v)=>s+v,0)/a.length,mb=b.reduce((s,v)=>s+v,0)/b.length;
  let xy=0,xx=0,yy=0;for(let i=0;i<a.length;i++){xy+=(a[i]-ma)*(b[i]-mb);xx+=(a[i]-ma)**2;yy+=(b[i]-mb)**2;}
  return xx&&yy?xy/Math.sqrt(xx*yy):null;
 }
 const sample=(rows,year,region='All')=>rows.filter(r=>r.year===year&&(region==='All'||r.region.trim()===region));
 function benchmark(rows,key){
  const p=rows.filter(r=>valid(r[key]));
  const covered=p.filter(r=>valid(r.population)),pop=covered.reduce((s,r)=>s+r.population,0);
  return {n:p.length,total:rows.length,median:median(p.map(r=>r[key])),weighted:pop?covered.reduce((s,r)=>s+r[key]*r.population,0)/pop:null};
 }
 const scaled=(value,divisor)=>valid(value)&&valid(divisor)&&divisor>0?value/divisor:null;
 const page=(rows,index=0,size=50)=>{const count=Math.max(1,Math.ceil(rows.length/size)),current=Math.max(0,Math.min(count-1,index));return {rows:rows.slice(current*size,(current+1)*size),index:current,count,total:rows.length};};
 const change=(a,b,key)=>a&&b&&valid(a[key])&&valid(b[key])?b[key]-a[key]:null;
 function thresholdSample(crossings,threshold,codes){
  const all=crossings.filter(r=>r.threshold===threshold&&codes.has(r.iso3));
  return {all,eligible:all.filter(r=>r.status==='observed'&&valid(r.gdp_ppp)&&r.gdp_ppp>0),counts:all.reduce((s,r)=>{s[r.status]=(s[r.status]||0)+1;return s;},{})};
 }
 function csv(rows,columns){
  const quote=v=>{let s=v==null?'':String(v);if(typeof v==='string'&&/^[\s]*[=+\-@]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';};
  return '\ufeff'+[columns.map(quote).join(','),...rows.map(r=>columns.map(c=>quote(r[c])).join(','))].join('\r\n');
 }
 const api={valid,median,pair,correlation,sample,benchmark,change,thresholdSample,csv,scaled,page};
 if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.AgingModel=api;
})(typeof window!=='undefined'?window:globalThis);
