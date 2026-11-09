"""Usage: python analysis/summarize_audit.py data/product_audit.csv data/brand_summary.csv
Adoption denominators = access_status=ok only; completeness only where product_jsonld_found=1. Wilson 95% CIs are descriptive."""
import csv, sys, math, collections
FIELDS = ["name","brand","description","image","price","priceCurrency","availability","identifier"]
def wilson(k, n, z=1.96):
    if n == 0: return ("", "")
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (round(c-h, 3), round(c+h, 3))
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8"))); by = collections.defaultdict(list)
for r in rows: by[r["store_brand"]].append(r)
out = []
for b, rs in by.items():
    ok = [r for r in rs if r["access_status"] == "ok"]; det = [r for r in ok if r["product_jsonld_found"] == "1"]
    fails = collections.Counter(r["access_status"] for r in rs if r["access_status"] != "ok")
    lo, hi = wilson(len(det), len(ok))
    d = dict(brand=b, urls=len(rs), fetched_ok=len(ok), detected=len(det),
             adoption=round(len(det)/len(ok), 3) if ok else "", adoption_ci_lo=lo, adoption_ci_hi=hi,
             mean_score=round(sum(float(r["score"]) for r in det)/len(det), 3) if det else "",
             access_failures=";".join(f"{k}:{v}" for k, v in fails.items()))
    for f in FIELDS: d["prev_"+f] = round(sum(int(r[f]) for r in det)/len(det), 3) if det else ""
    out.append(d)
with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print("brands:", len(out))
