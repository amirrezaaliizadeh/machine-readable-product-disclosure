(async()=>{
const URLS=__URLS__;
const FIELDS=["name","brand","description","image","price","priceCurrency","availability","identifier"];
const types=n=>{let t=n["@type"]||[];t=typeof t==="string"?[t]:t;return t.map(x=>String(x).split("/").pop())};
const present=v=>{if(v==null)return false;if(Array.isArray(v))return v.some(present);if(typeof v==="object")return Object.entries(v).some(([k,x])=>!k.startsWith("@")&&present(x))||!!v["@id"];return String(v).trim()!==""};
function* walk(x){if(Array.isArray(x)){for(const i of x)yield*walk(i)}else if(x&&typeof x==="object"){yield x;for(const k of["@graph","mainEntity","hasVariant","itemListElement","item"])if(k in x)yield*walk(x[k])}}
const offersOf=n=>{let o=n.offers;const out=[];for(const it of(Array.isArray(o)?o:o?[o]:[])){if(it&&typeof it==="object"){out.push(it);if(Array.isArray(it.offers))for(const j of it.offers)if(j&&typeof j==="object")out.push(j)}}return out};
const ps=(o,k)=>o.priceSpecification&&typeof o.priceSpecification==="object"?o.priceSpecification[k]:null;
function score(p){const cands=types(p).includes("ProductGroup")?[p,...(Array.isArray(p.hasVariant)?p.hasVariant.filter(v=>v&&typeof v==="object"):[])]:[p];const offers=cands.flatMap(offersOf);const any=(keys,nodes)=>nodes.some(n=>keys.some(k=>present(n[k])));
const f={name:any(["name"],[p]),brand:any(["brand"],cands),description:any(["description"],cands),image:any(["image"],cands),price:offers.some(o=>present(o.price)||present(o.lowPrice)||present(ps(o,"price"))),priceCurrency:offers.some(o=>present(o.priceCurrency)||present(ps(o,"priceCurrency"))),availability:offers.some(o=>present(o.availability)),identifier:any(["sku","mpn","gtin","gtin8","gtin12","gtin13","gtin14","productID"],cands)};
const r={};for(const k of FIELDS)r[k]=f[k]?1:0;return r}
function extract(html){const d=new DOMParser().parseFromString(html,"text/html");let blocks=[],err=0;d.querySelectorAll("script").forEach(s=>{if(/ld\+json/i.test(s.getAttribute("type")||"")){try{blocks.push(JSON.parse(s.textContent.trim()))}catch(e){err++}}});
const nodes=[...walk(blocks)];const prods=nodes.filter(n=>types(n).some(t=>t==="Product"||t==="ProductGroup"));const base={blocks:blocks.length,err,cands:prods.length};
if(!prods.length)return{...base,found:0,s:null,score:""};let best=null,bs=-1;for(const n of prods){const s=score(n);const t=FIELDS.reduce((a,k)=>a+s[k],0);if(t>bs){bs=t;best=s}}
const first=score(prods[0]);return{...base,found:1,s:best,score:bs/8,firstScore:FIELDS.reduce((a,k)=>a+first[k],0)/8}}
const challenge=h=>{const l=h.toLowerCase();return h.length<6000&&!l.includes("<title")&&!l.includes("ld+json")&&l.includes("<script")&&!l.includes("<h1")};
const sha=async t=>[...new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(t)))].map(b=>b.toString(16).padStart(2,"0")).join("");
// robots
let rob={status:"robots_unavailable",rules:[],delay:0};
try{const r=await fetch(location.origin+"/robots.txt");if(r.ok){const t=await r.text();let grp=[],cur=null,ins=false,delay=0;let star=false;for(const raw of t.split(/\r?\n/)){const line=raw.split("#")[0].trim();if(!line)continue;const i=line.indexOf(":");if(i<0)continue;const k=line.slice(0,i).trim().toLowerCase(),v=line.slice(i+1).trim();if(k==="user-agent"){if(!ins){star=false}ins=true;if(v==="*")star=true}else{ins=false;if(star){if(k==="disallow")grp.push(["d",v]);else if(k==="allow")grp.push(["a",v]);else if(k==="crawl-delay")delay=parseFloat(v)||0}}}rob={status:"ok",rules:grp,delay}}else if(r.status>=400&&r.status<500){rob={status:"ok_no_robots_4xx",rules:[],delay:0}}}catch(e){}
const allowed=p=>{let best=null,bl=-1;for(const[t,v]of rob.rules){if(!v)continue;const re=new RegExp("^"+v.replace(/[.+?^${}()|[\]\\]/g,"\\$&").replace(/\*/g,".*").replace(/\\\$$/,"$"));if(re.test(p)&&v.length>bl){bl=v.length;best=t}}return best!=="d"};
const out=[];
for(const u of URLS){const row={url:u,access:"",http:"",final:"",len:"",sha:"",blocks:"",err:"",cands:"",found:"",s:null,score:"",firstScore:""};const pth=new URL(u).pathname;
if(rob.status==="robots_unavailable")row.access="robots_unavailable";else if(!allowed(pth))row.access="robots_disallowed";else{await new Promise(r=>setTimeout(r,Math.max(2500,rob.delay*1000)));
try{const r=await fetch(u);row.http=r.status;row.final=r.url;const ct=r.headers.get("content-type")||"";const t=await r.text();row.len=t.length;row.sha=await sha(t);
if(!r.ok)row.access="fetch_error";else if(!/html/i.test(ct))row.access="non_html";else if(challenge(t))row.access="bot_challenge";else{row.access="ok";Object.assign(row,extract(t))}}catch(e){row.access="fetch_error";row.http=String(e).slice(0,40)}}
out.push(row)}
window.__out=out;
return {robots:{status:rob.status,nRules:rob.rules.length,delay:rob.delay},rows:out.map(r=>[r.url.replace(location.origin,"").slice(-60),r.access,r.http,r.len,r.blocks,r.cands,r.found,r.s?FIELDS.map(k=>r.s[k]).join(""):"",r.score===""?"":+r.score.toFixed(3),r.firstScore===""?"":+(+r.firstScore).toFixed(3),r.final&&r.final.split("?")[0]!==r.url?"REDIR:"+r.final.replace(location.origin,"").slice(0,50):"",(r.sha||"").slice(0,12)].join(","))};
})()
