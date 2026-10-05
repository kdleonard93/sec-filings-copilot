# Architecture decision record

Each decision names the alternative that was rejected and why. The rejections are the point: they are the part a vendor page cannot give you.

## Active decisions

| Decision | Chosen | Rejected and why |
| --- | --- | --- |
| Corpus retrieval | Hybrid ON, reranker OFF (v1) | A reranker adds latency, and filing queries contain exact tokens (ticker, "segment 7"), so hybrid is required. Reranker revisited at scale in the Phase 6 retro. Fine-tuned embeddings are a later iteration. |
| Chunking | Table-aware plus parent-document | Fixed-size alone splits tables across chunk boundaries, corrupting rows and columns. |
| Per-record data | Genie over the watch-list table | A vector corpus cannot answer per-record facts. This is the most-tested misconception in the domain. |
| Extracted numbers | Separate extraction pipeline into a KPI Delta table | Re-reading a 200-page PDF per question is slower, costlier, and unauditable versus a queryable table. |
| Shape | Agent with 3 tools, not a chain | The question type determines the source and is unknowable ahead of time. |
| LLM | Foundation Model APIs default, OpenRouter external-model endpoint swappable | Portability and budget. The judge is kept in a different model family from the generator for eval validity. |
| Fine-tuning | Explicitly rejected in favor of retrieval | Facts change and are citation-bound; retrieval wins for changing facts. Standing rejection, not a deferred task. |

## Standing rejections

- **Fine-tuning a base model.** The corpus changes and every claim needs a citation, so retrieval is the correct instrument. Recorded here so it is not relitigated per phase.
- **A chain instead of an agent.** Any fixed pipeline hard-codes an assumption about the question source that the corpus violates.
- **A vector index for per-record facts.** Watch-list lookups are structured lookups and belong in Genie.
- **Reranker in v1.** Latency cost is not justified before the retrieval baseline is measured. Revisit with numbers in Phase 6.

## How decisions get added

New rows are added when a phase surfaces a real tradeoff, especially a Free Edition limit. Each limit hit during the build becomes a row here, not a blocker in a chat thread.
