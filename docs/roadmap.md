# Roadmap

## Build order

Phases are built in order; each consumes the previous phase's output. Status is tracked in the [README](../README.md#project-status).

1. **Lab 0** - workspace, schemas, repo.
2. **Phase 1** - ingestion, cleaning, chunking (`chunks_v1`, `chunks_v2`), AI Search index.
3. **Phase 2** - KPI extraction, Genie space, RAG chain, 3-tool agent.
4. **Phase 3** - UC model registration, serving endpoint, prompt promotion, batch inference.
5. **Phase 4** - PII masking, guardrails, provenance.
6. **Phase 5** - labeled eval, scorer suite, promotion gate, monitoring.
7. **Phase 6** - case-study write-up and release.

The exam-critical path ends at Phase 5. The layer below is optional portfolio work added afterward.

## Post-cert: the decision layer

The decision model runs locally via `ollama pull nimble`, so the component that decides whether to escalate also runs on-device. That strengthens the governance story: no filing, document, or query leaves the machine.

- **Retrieval upgrade (attaches to Phase 2).** Re-rank with a single Choice question over pre-trimmed candidates (k around 20), never N independent Score calls, because separate questions are not on a shared scale. Gate with a Noul relevance question whose threshold is tuned on the labeled set.
- **Judge upgrade (attaches to Phase 5).** Add a third, different model family as an independent judge and report inter-judge agreement. A chat model writes the rationale; the decision model supplies the number.
- **Repo safety.** Keep a `--no-judge` escape so the harness runs without Ollama, pin the model version, and log the returned model string per run.

## Same architecture, other platforms

Only the bindings are platform-specific. The client brief, scoping, ADR, ops log, and case-study wrapper are platform-neutral. Six integration points change:

| Phase | Databricks binding | Equivalent |
| --- | --- | --- |
| Ingestion and index | Delta table plus AI Search (HNSW, BM25 plus RRF) | Snowflake Cortex Search, BigQuery `VECTOR_SEARCH`, pgvector or Qdrant |
| Chain and agent | LangChain or LangGraph on Model Serving plus Genie | Snowflake Cortex Agents, Vertex Agent Engine, Bedrock Agents |
| Deploy and promote | Model Serving plus MLflow prompt registry | Vertex Model Garden, Fireworks or Together, the OpenRouter swap |
| Governance | Unity Catalog (lineage, RBAC, tags, masks) | Snowflake Horizon, Google Knowledge Catalog, Microsoft Purview |
| Eval and monitoring | MLflow GenAI scorers plus inference tables | DeepEval plus Langfuse or Arize Phoenix |

## Interview script

> "I built and evaluated this on Databricks end to end: ingestion, retrieval, agent, governance, online eval. Here is the same architecture on Snowflake and on a serverless OSS stack, and here is what I would check first in your environment: where the data already lives, what the catalog enforces, whether the serving API is OpenAI-compatible, and the GPU utilization before anyone suggests self-hosting."
