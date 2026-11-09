"""Robots-aware collector. Usage: python analysis/collect_product_markup.py --frame data/product_urls.csv --output data/product_audit.csv --delay 2 --contact you@campus.unimib.it
Frame CSV columns: brand,url,gender_stratum. Run ONLY after supervisor approval and from a network that can reach the sites."""
import argparse, csv, hashlib, time, datetime, urllib.request, urllib.error, urllib.robotparser, urllib.parse, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from markup_extract import extract, FIELDS, looks_like_bot_challenge

def robots_status(base, ua, cache, timeout=15):
    """RFC 9309: 2xx parse; 4xx = no restrictions; 5xx/unreachable = treat as disallowed (recorded separately)."""
    if base in cache: return cache[base]
    rp = urllib.robotparser.RobotFileParser(); url = base + "/robots.txt"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        with urllib.request.urlopen(req, timeout=timeout) as r: rp.parse(r.read().decode("utf-8", "replace").splitlines()); res = ("ok", rp)
    except urllib.error.HTTPError as e:
        res = ("ok_no_robots_4xx", None) if 400 <= e.code < 500 else ("robots_unavailable", None)
    except Exception: res = ("robots_unavailable", None)
    cache[base] = res; return res

def run(frame, out, delay, ua):
    cache, seen, rows = {}, set(), []
    for r in csv.DictReader(open(frame, encoding="utf-8")):
        url = r["url"].strip(); row = dict(store_brand=r["brand"], url=url, gender_stratum=r.get("gender_stratum", ""),
            fetched_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            access_status="", http_status="", final_url="", sha256="")
        if url in seen: row["access_status"] = "duplicate_url"; rows.append(row); continue
        seen.add(url); pu = urllib.parse.urlparse(url); base = f"{pu.scheme}://{pu.netloc}"
        st, rp = robots_status(base, ua, cache)
        if st == "robots_unavailable": row["access_status"] = st
        elif rp is not None and not rp.can_fetch(ua, url): row["access_status"] = "robots_disallowed"
        else:
            wait = (rp.crawl_delay(ua) if rp else None) or delay; time.sleep(max(wait, delay))
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "it-IT,it;q=0.9"}), timeout=30) as resp:
                    ct = resp.headers.get("Content-Type", ""); body = resp.read(); row.update(http_status=resp.status, final_url=resp.geturl())
                if "html" not in ct.lower(): row["access_status"] = "non_html"
                else:
                    txt = body.decode("utf-8", "replace"); row["sha256"] = hashlib.sha256(body).hexdigest()
                    if looks_like_bot_challenge(txt): row["access_status"] = "bot_challenge"  # observed, not scored, never bypassed
                    else: row["access_status"] = "ok"; row.update(extract(txt))
            except urllib.error.HTTPError as e: row.update(access_status="fetch_error", http_status=e.code)
            except Exception as e: row.update(access_status="fetch_error", http_status=type(e).__name__)
        rows.append(row)
    cols = ["store_brand","url","gender_stratum","fetched_at","access_status","http_status","final_url","sha256","jsonld_blocks","jsonld_parse_errors","product_candidates","product_jsonld_found"] + FIELDS + ["score"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--frame", required=True); ap.add_argument("--output", required=True)
    ap.add_argument("--delay", type=float, default=2.0); ap.add_argument("--contact", required=True)
    a = ap.parse_args(); run(a.frame, a.output, a.delay, f"UniMiB-ProductDisclosureAudit/1.0 (academic research; contact: {a.contact})")
