import csv, math, json, collections
FIELDS=["name","brand","description","image","price","priceCurrency","availability","identifier"]
BR=["Nike","Adidas","New Balance","ASICS","On","Under Armour"]
sample=list(csv.DictReader(open("sample_manifest.csv")))
frame=list(csv.DictReader(open("frame_manifest.csv")))
raw={b:[l.split(",") for l in open(f"raw/{b}.txt").read().strip().split("\n")] for b in BR}
rows=[]
for b in BR:
    s=[r for r in sample if r["brand"]==b]; assert len(s)==len(raw[b])==20
    for i,(m,x) in enumerate(zip(s,raw[b])):
        access,http,ln,blocks,cands,found,fl,score,first,redir,sha=x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11]
        # pass 2 (top-level-node-only score; plain-client condition)
        if b in("Nike","On","New Balance"): strict="11100000"
        elif b=="Adidas": strict="11111111" if m["url"].endswith(("JQ7697.html","IF9390.html")) else "11100000"
        else: strict="11111111"
        plain="bot_challenge" if b in("Adidas","New Balance") else "ok"
        hasgroup=0 if m["url"].endswith(("JQ7697.html","IF9390.html")) else 1
        d=dict(store_brand=b,url=m["url"],gender_stratum=m["gender_stratum"],access_status=access,http_status=http,html_bytes=ln,jsonld_blocks=blocks,product_nodes_incl_variants=cands,product_jsonld_found=found,**{'f_'+f:int(c) for f,c in zip(FIELDS,fl)},score_variant_aware=score,score_first_node=first,sha256_prefix=sha,top_level_fields="".join(strict),score_top_level_only=round(sum(map(int,strict))/8,3),has_productgroup=hasgroup,plain_client_access=plain)
        rows.append(d)
with open("audit_120_pages.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def wil(k,n,z=1.96):
    p=k/n; dd=1+z*z/n; c=(p+z*z/(2*n))/dd; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/dd; return (max(0,c-h),min(1,c+h))
S={}
for b in BR+["All"]:
    rs=[r for r in rows if b=="All" or r["store_brand"]==b]; n=len(rs)
    ok=[r for r in rs if r["access_status"]=="ok"]; det=[r for r in ok if r["product_jsonld_found"]=="1"]
    lv=[float(r["score_variant_aware"]) for r in det]; st=[r["score_top_level_only"] for r in det]
    pl=sum(r["plain_client_access"]=="ok" for r in rs)
    S[b]=dict(n=n,ok=len(ok),det=len(det),adopt=len(det)/len(ok),adopt_ci=wil(len(det),len(ok)),mean_lenient=sum(lv)/len(lv),mean_strict=sum(st)/len(st),
      strict_full=sum(1 for x in st if x==1.0),plain=pl,plain_ci=wil(pl,n),group=sum(r["has_productgroup"] for r in det),
      strictprev={f:sum(int(r["top_level_fields"][i]) for r in det)/len(det) for i,f in enumerate(FIELDS)},
      men=sum(r["gender_stratum"]=="M" for r in rs),women=sum(r["gender_stratum"]=="W" for r in rs),
      first_equal=sum(1 for r in det if r["score_first_node"]==r["score_variant_aware"]),
      nodes_med=sorted(int(r["product_nodes_incl_variants"]) for r in det)[len(det)//2], bytes_med=sorted(int(r["html_bytes"]) for r in rs)[n//2])
fr={}
for b in BR:
    for s in "MW":
        fr[(b,s)]=sum(1 for r in frame if r["brand"]==b and r["stratum"]==s and r["frame_status"]=="eligible")
fexcl=collections.Counter((r["brand"],r["reason"]) for r in frame if r["frame_status"]=="excluded")
json.dump({"S":S,"frame":{f"{k[0]}|{k[1]}":v for k,v in fr.items()},"fexcl":{f"{k[0]}|{k[1]}":v for k,v in fexcl.items()}},open("summary.json","w"),indent=1,default=str)
for b,v in S.items(): print(b,v["n"],v["ok"],v["det"],round(v["adopt"],3),[round(x,3) for x in v["adopt_ci"]],round(v["mean_lenient"],3),round(v["mean_strict"],3),"plain",v["plain"],[round(x,3) for x in v["plain_ci"]],"group",v["group"],"M/W",v["men"],v["women"],"first=",v["first_equal"],"nodes_med",v["nodes_med"],"bytes_med",v["bytes_med"])
print(fr); print(fexcl)
# figures
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
fig,ax=plt.subplots(1,2,figsize=(11,4.2),gridspec_kw={"width_ratios":[1.5,1]})
M=np.array([[S[b]["strictprev"][f] for f in FIELDS] for b in BR]); im=ax[0].imshow(M,cmap="Blues",vmin=0,vmax=1,aspect="auto")
ax[0].set_xticks(range(8)); ax[0].set_xticklabels(FIELDS,rotation=35,ha="right",fontsize=9); ax[0].set_yticks(range(6)); ax[0].set_yticklabels(BR,fontsize=10)
for i in range(6):
    for j in range(8): ax[0].text(j,i,f"{M[i,j]*100:.0f}",ha="center",va="center",color="white" if M[i,j]>0.6 else "black",fontsize=9)
ax[0].set_title("(a) Fields present in the top-level Product/ProductGroup node (%)",fontsize=10)
x=np.arange(6); ax[1].bar(x-0.2,[100]*6,0.4,label="Browser session",color="#3b6ea5"); ax[1].bar(x+0.2,[S[b]["plain"]/S[b]["n"]*100 for b in BR],0.4,label="No-cookie request",color="#e08e45")
ax[1].set_xticks(x); ax[1].set_xticklabels(BR,rotation=35,ha="right",fontsize=9); ax[1].set_ylabel("Pages returning product HTML (%)"); ax[1].set_ylim(0,110); ax[1].legend(fontsize=8,loc="lower left"); ax[1].set_title("(b) Access to product HTML",fontsize=10)
plt.tight_layout(); plt.savefig("figure1.png",dpi=200)
