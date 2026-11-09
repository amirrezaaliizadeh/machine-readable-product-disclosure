"""Offline JSON-LD extraction for the product-disclosure audit (stdlib only)."""
import json, re
from html.parser import HTMLParser

FIELDS = ["name", "brand", "description", "image", "price", "priceCurrency", "availability", "identifier"]

class _LD(HTMLParser):
    def __init__(self):
        super().__init__(); self.in_ld = False; self.buf = []; self.blocks = []; self.errors = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and "ld+json" in (a.get("type") or "").lower():
            self.in_ld = True; self.buf = []
    def handle_data(self, d):
        if self.in_ld: self.buf.append(d)
    def handle_endtag(self, tag):
        if tag == "script" and self.in_ld:
            self.in_ld = False
            raw = "".join(self.buf).strip()
            try: self.blocks.append(json.loads(raw))
            except Exception: self.errors += 1

def _walk(x):
    if isinstance(x, list):
        for i in x: yield from _walk(i)
    elif isinstance(x, dict):
        yield x
        for k, v in x.items():
            if k in ("@graph", "mainEntity", "hasVariant", "itemListElement", "item"): yield from _walk(v)

def _types(n):
    t = n.get("@type", []); t = [t] if isinstance(t, str) else t
    return {str(i).split("/")[-1] for i in t}

def _present(v):
    if v is None: return False
    if isinstance(v, (list, tuple)): return any(_present(i) for i in v)
    if isinstance(v, dict): return any(_present(i) for k, i in v.items() if not k.startswith("@")) or bool(v.get("@id"))
    return str(v).strip() != ""

def _offers(n):
    o = n.get("offers"); out = []
    for item in (o if isinstance(o, list) else [o] if o else []):
        if isinstance(item, dict):
            out.append(item)
            out.extend(i for i in (item.get("offers") or []) if isinstance(i, dict)) if isinstance(item.get("offers"), list) else None
    return out

def score_node(prod):
    """Eight binary fields. For ProductGroup, variants are searched too (rule documented in protocol v2)."""
    cands = [prod] + [v for v in (prod.get("hasVariant") or []) if isinstance(v, dict)] if "ProductGroup" in _types(prod) else [prod]
    offers = [o for c in cands for o in _offers(c)]
    def any_of(keys, nodes): return any(_present(n.get(k)) for n in nodes for k in keys)
    f = {
        "name": any_of(["name"], [prod]), "brand": any_of(["brand"], cands),
        "description": any_of(["description"], cands), "image": any_of(["image"], cands),
        "price": any(_present(o.get("price")) or _present(o.get("lowPrice")) or _present((o.get("priceSpecification") or {}).get("price") if isinstance(o.get("priceSpecification"), dict) else None) for o in offers),
        "priceCurrency": any(_present(o.get("priceCurrency")) or _present((o.get("priceSpecification") or {}).get("priceCurrency") if isinstance(o.get("priceSpecification"), dict) else None) for o in offers),
        "availability": any(_present(o.get("availability")) for o in offers),
        "identifier": any_of(["sku", "mpn", "gtin", "gtin8", "gtin12", "gtin13", "gtin14", "productID"], cands),
    }
    return {k: int(v) for k, v in f.items()}

def extract(html):
    p = _LD(); p.feed(html)
    nodes = [n for b in p.blocks for n in _walk(b)]
    prods = [n for n in nodes if _types(n) & {"Product", "ProductGroup"}]
    base = dict(jsonld_blocks=len(p.blocks), jsonld_parse_errors=p.errors, product_candidates=len(prods))
    if not prods:
        return {**base, "product_jsonld_found": 0, **{k: "" for k in FIELDS}, "score": ""}
    best = max(prods, key=lambda n: sum(score_node(n).values()))  # most complete node; ties -> first
    s = score_node(best)
    return {**base, "product_jsonld_found": 1, **s, "score": round(sum(s.values()) / 8, 3)}


def looks_like_bot_challenge(html):
    """Heuristic: tiny script-only interstitial (no <title>, no JSON-LD). Record as access_status=bot_challenge; never bypass."""
    h = html.lower()
    return len(html) < 6000 and "<title" not in h and "ld+json" not in h and "<script" in h and "<h1" not in h
