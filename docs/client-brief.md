# Client brief

*(Simulated engagement, written as a real one. A hiring manager should not be able to tell it was not. Real client work gets the identical format.)*

## Client

"Meridian Research," a boutique equity-research shop with four analysts. They cover roughly 30 mid-cap public companies and compete on speed: analysts read filings the day they drop, before the street.

## Their data

- 10-Ks, 10-Qs, and 8-Ks from EDGAR: 200-page PDFs with financial tables, exhibits, and footnotes.
- Earnings-call transcripts.
- A small internal watch-list table (ticker, sector, analyst owner, status) in a warehouse.

## The outcome they need

An analyst asks a plain-English question such as:

> "What changed in Acme's risk factors about supply-chain concentration between the 2024 and 2025 10-K?"

...and gets a grounded, cited answer in seconds, plus the structured numbers in a queryable table. Per-record questions ("What's our current rating on ACME?") come from the warehouse, never from the document corpus.

## Why this is a realistic deployment

Three data types are in play: unstructured prose, tables embedded in documents, and structured warehouse records. Each requires a different retrieval mechanism. Sending a per-record question to a vector index, or asking a document corpus for a number that belongs in a table, are the exact wrong-tool failures this project is designed to route around. That mapping is the core design decision, not a detail.
