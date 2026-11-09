Replication package: Machine-Readable Product Disclosure on Brand-Owned Websites (collected 15 Oct 2026, Europe/Rome)

audit_120_pages.csv   URL-level results (store_brand, url, gender_stratum, access_status, http_status, html_bytes, jsonld_blocks, product_nodes_incl_variants, product_jsonld_found, f_<field> x8, score_variant_aware, score_first_node, sha256_prefix, top_level_fields, score_top_level_only, has_productgroup, plain_client_access)
frame_manifest.csv    every eligible/excluded record in the frame (brand, stratum, code, URL, status, reason)
sample_manifest.csv   the 120 sampled URLs (seed 20261015)
frame.py              builds frame and draws the sample (random.Random(20261015), eligible URLs sorted alphabetically)
analyze.py            builds audit CSV, Wilson intervals, Figure 1
summary.json          computed summary statistics
figure1.png           Figure 1
Code for extraction (markup_extract.py, tests, collector) is in the code folder of the same package.

Data collection method: in-page JavaScript run in a desktop browser on the brand's own origin (see manuscript Section 3.3). robots.txt was fetched first and obeyed; >= 2.5 s between requests. Page HTML is not redistributed.
Note: columns f_name ... f_identifier are the variant-aware field indicators; top_level_fields is an 8-character string in the same field order for the top-level-node-only reading.
browser_collector_reference.js  reference version of the in-browser collector (primary pass); the second pass (top-level scoring, no-cookie request) used the same parsing with fetch(url,{credentials:'omit'}).
