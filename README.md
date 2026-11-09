# Machine-Readable Product Disclosure: replication package

Code and data for an audit of machine-readable product disclosure (schema.org / JSON-LD markup) on product pages of Italian running-shoe brand websites.

- `code/`: robots-aware collector, markup extraction, audit summary and unit tests.
- `data-and-replication/`: sampling frame, audit results for 120 pages, reliability and cross-browser checks, analysis scripts and figures. See its README for the run order.

The collector identifies itself with a user agent and a contact address you supply at run time (`--contact`); no personal contact details are stored in this repository.
