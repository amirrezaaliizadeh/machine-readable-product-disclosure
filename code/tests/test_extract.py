import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "analysis"))
from markup_extract import extract, looks_like_bot_challenge
def page(j): return f'<html><head><script type="application/ld+json">{j}</script></head></html>'
FULL = '{"@type":"Product","name":"X","brand":{"@type":"Brand","name":"B"},"description":"d","image":["i.jpg"],"sku":"1","offers":{"@type":"Offer","price":"99.9","priceCurrency":"EUR","availability":"https://schema.org/InStock"}}'
class T(unittest.TestCase):
    def test_full(self): self.assertEqual(extract(page(FULL))["score"], 1.0)
    def test_graph(self): self.assertEqual(extract(page('{"@graph":[{"@type":"WebPage"},'+FULL+']}'))["product_jsonld_found"], 1)
    def test_missing(self): self.assertEqual(extract(page('{"@type":"WebPage"}'))["product_jsonld_found"], 0)
    def test_zero_price(self): self.assertEqual(extract(page(FULL.replace('"99.9"','0')))["price"], 1)
    def test_multiple_picks_complete(self):
        r = extract(page('[{"@type":"Product","name":"stub"},'+FULL+']')); self.assertEqual((r["product_candidates"], r["score"]), (2, 1.0))
    def test_productgroup_variants(self):
        g = '{"@type":"ProductGroup","name":"G","brand":"B","description":"d","image":"i","hasVariant":[{"@type":"Product","sku":"1","offers":[{"@type":"Offer","price":"5","priceCurrency":"EUR","availability":"InStock"}]}]}'
        self.assertEqual(extract(page(g))["score"], 1.0)
    def test_aggregate_offer(self):
        p = '{"@type":"Product","name":"n","offers":{"@type":"AggregateOffer","lowPrice":"5","priceCurrency":"EUR"}}'
        r = extract(page(p)); self.assertEqual((r["price"], r["priceCurrency"], r["availability"]), (1, 1, 0))
    def test_broken_json(self): self.assertEqual(extract(page('{bad'))["jsonld_parse_errors"], 1)
    def test_empty_values(self): self.assertEqual(extract(page('{"@type":"Product","name":" ","sku":""}'))["name"], 0)
class C(unittest.TestCase):
    def test_challenge(self): self.assertTrue(looks_like_bot_challenge('<!DOCTYPE html><html><body><script src="/x.js"></script></body></html>'))
    def test_real_page_not_challenge(self): self.assertFalse(looks_like_bot_challenge(page(FULL)))
if __name__ == "__main__": unittest.main()
