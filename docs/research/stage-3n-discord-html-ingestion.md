# Stage 3N Discord HTML Ingestion

Stage 3N ingests admin-provided local Discord HTML archives as a privacy-preserving
source-discovery layer.

The local run scanned 42 HTML files and 465845099 bytes. It found 386511 extracted links across
2224 unique domains, 38647 attachment candidates, 48107 method-claim candidates, 67660 numeric
observation candidates, and 7324 known-bogus/debunked or tried-and-failed claim candidates.

The outputs are review aids only:

- full extracted records remain ignored;
- local review HTML remains ignored;
- raw Discord logs remain ignored;
- message bodies and usernames are not committed;
- no live Discord API, scraping, AI upload, CUDA, or solve claim is made.

The next safe step is to review selected public links and promote only vetted public sources or
observations into the existing source registry.
