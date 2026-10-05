# SEC Filings Research Copilot

A governed RAG research copilot over SEC EDGAR filings, built and evaluated end to end on Databricks Free Edition. Analysts ask plain-English questions of 10-K, 10-Q, and 8-K filings and get grounded, cited answers in seconds, plus structured financials in queryable tables.

![status](https://img.shields.io/badge/status-in%20progress-yellow)
![platform](https://img.shields.io/badge/platform-Databricks%20Free%20Edition-red)
![license](https://img.shields.io/badge/license-MIT-blue)

**Status:** active build. Lab 0 (workspace, schemas, repo) is complete; Phases 1 through 6 are in progress. This README is the front door. The build plan, decisions, and operations log live in [`docs/`](docs/).

---

## What it does

- **Document Q&A.** Hybrid search (vector plus keyword) over a table-aware chunk index, with a citation on every claim.
- **Structured extraction.** A validated pipeline turns filings into a KPI table (segment revenue, operating margin, headcount by fiscal year).
- **Record lookup.** A Genie space answers watch-list questions from the warehouse table, not the corpus.
- **Routing.** One agent picks the right source per question, because the question type is unknowable ahead of time.
- **Refusal.** Out-of-context and investment-advice questions are refused by design.
- **Measured quality.** Every quality claim comes from a labeled eval set and a scorer suite, not a demo.

---

## Quickstart

### Prerequisites

- A [Databricks Free Edition](https://www.databricks.com/learn/free-edition) workspace (serverless only, no card required).
- Python 3.10+ for the local harness.
- Git, and a GitHub account for the Git-folder workflow.

### 1. Workspace and schemas

Confirm the catalog name first. Free Edition uses `workspace`, not `main`.

Run the setup notebook: [`notebooks/SEC_Filings.py`](notebooks/SEC_Filings.py).

```python
display(spark.sql("SHOW CATALOGS"))
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.sec_lab")   # documents
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.finance")   # business tables
```

Then confirm foundation-model access in **AI/ML -> Playground** by sending a trivial prompt.

### 2. Environment variables

Model and provider choices are config values, never hard-coded, so a provider swap is a config change:

```
LLM_BASE_URL / LLM_MODEL / LLM_API_KEY                  # chat stack
DECISION_ENABLED / DECISION_MODEL / DECISION_BASE_URL   # post-cert decision layer
```

Secrets (API keys, PATs) live in Databricks Secrets or a local `.env`, never in the repo.

### 3. Build order

Phases are built in order, each consuming the previous phase's output. See [`docs/roadmap.md`](docs/roadmap.md) for the phase detail and the post-cert layer. Notebooks run natively in the Databricks Git folder.

---

## Architecture

```
EDGAR filings (PDF / HTML) ──► UC Volume (raw)
      │
      ▼  Phase 1 - ingest and index
   parse, clean, chunk, dedupe
   chunks_v1 (recursive baseline) · chunks_v2 (table-aware)   [CDF ON]
      ├──► AI Search Delta Sync index (hybrid ON, reranker OFF v1)
      └──► KPI extraction ──► workspace.finance.kpis
      │
      ▼  Phase 2 - orchestrate
   chat agent, 3 tools:
     filings search   · Genie watch-list lookup   · KPI table query
   grounding, citation post-processing, refusal path
      │
      ▼  Phase 3 - serve
   Model Serving endpoint + AI Gateway inference table
   MLflow Prompt Registry (prompt v1 -> @champion)
      │
      ▼  Phase 5 - evaluate and monitor
   mlflow.genai.evaluate() + promotion gate + usage and latency tables
```

---

## Repository layout

```
sec-filings-copilot/
├── README.md          # this file
├── notebooks/         # Databricks notebooks (edited in the Git folder)
├── sql/               # DDL and queries
├── docs/              # brief, scoping, ADR, ops log, roadmap
├── evals/             # labeled eval set and results
├── harness/           # local eval harness (post-cert: decision layer)
└── LICENSE
```

Bulk data and secrets stay out of the repo (see `.gitignore`).

---

## Evaluation

Quality is measured against a 25-question labeled set, from an SME's perspective, plus relevant-chunk labels for 10. Scorers are the built-in `Correctness`, `RetrievalGroundedness`, and `RetrievalRelevance`, plus custom `has_citation` and `no_advice`. Both chunking versions (`chunks_v1`, `chunks_v2`) are run against the same set to produce a version-by-scorer table. The eval becomes a pass or fail promotion gate, and live inference-table traffic is scored offline and sampled into the next eval set.

---

## Design decisions

The full record, with context and standing rejections, is in [`docs/adr.md`](docs/adr.md). Summary:

| Decision | Rejected and why |
| --- | --- |
| Hybrid retrieval, reranker off (v1) | A reranker adds latency, and ticker or exact-token queries need keyword search anyway |
| Table-aware plus parent-document chunking | Fixed-size alone splits tables across chunk boundaries |
| Genie for per-record facts | A vector corpus cannot answer per-record facts |
| Extraction pipeline into a KPI table | Re-reading a 200-page PDF per question is slower and unauditable |
| Agent with 3 tools | A chain cannot know the source ahead of time |
| Foundation Model APIs default, OpenRouter swappable | Lock-in and budget; the judge stays cross-family for eval validity |
| Retrieval, not fine-tuning | Facts change and are citation-bound |

---

## Project status

| Phase | Scope | Status |
| --- | --- | --- |
| **Lab 0** | Workspace, schemas, git repo, GitHub remote | Done |
| **Phase 1** | Ingestion, cleaning, chunking (v1 and v2), AI Search index | In progress |
| **Phase 2** | KPI extraction, Genie space, RAG chain, 3-tool agent | Planned |
| **Phase 3** | UC model registration, serving endpoint, prompt promotion, batch inference | Planned |
| **Phase 4** | PII masking, guardrails, provenance | Planned |
| **Phase 5** | Labeled eval, scorer suite, promotion gate, monitoring | Planned |
| **Phase 6** | Case-study write-up and release | Planned |
| **Post-cert** | Local decision layer (Nimble via Ollama) beside the harness | Planned |

---

## Docs

- [Client brief](docs/client-brief.md) - the engagement this system answers.
- [Scoping](docs/scoping.md) - in scope, out of scope, constraints, and limitations.
- [Architecture decision record](docs/adr.md) - decisions and rejected alternatives.
- [Operations log](docs/operations-log.md) - failures and fixes from the build.
- [Roadmap](docs/roadmap.md) - phase detail, the post-cert decision layer, and cross-platform equivalents.

---

## License

MIT. See [LICENSE](LICENSE).
