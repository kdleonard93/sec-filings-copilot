# Scoping

Written as it would be handed to a client. Skipping scoping is the first and most common deployment rejection pattern, so it is never skipped here.

## In scope

- RAG over a roughly 10-filing corpus (2 to 3 issuers, each with a 10-K, a 10-Q, and the latest 8-K), stored in a Unity Catalog Volume.
- Information-extraction pipeline: filings to segment-revenue and KPI Delta tables ("structured numbers").
- Genie space over the watch-list table for per-record lookups.
- Single agent routing: document RAG, Genie records, or the extracted KPI table.
- Serving endpoint, AI Gateway inference tables, Prompt Registry promotion, eval harness, and monitoring.
- Governance: PII masking, guardrails, and license and provenance metadata.

## Out of scope

- **Investment-advice outputs.** A disclaimer layer only.
- **Real-time pricing.** EDGAR and daily snapshots only.
- **Multi-tenancy.**
- **Fine-tuning a base model.** Retrieval wins for changing, citation-bound facts. Fine-tuning stays a standing rejected alternative in [the ADR](adr.md).

## Constraints

- Free Edition compute: serverless only, roughly 10 filings and 3,000 chunks.
- Token spend capped per the budget guardrails in the companion study guide.
- Each phase sized for 2 to 5 evening sessions.

## Known constraints and limitations

- **Corpus size is deliberately small.** Free Edition compute caps the build at roughly 10 filings and 3,000 chunks. That proves the method, not production volume.
- **Free Edition limits are recorded, not hidden.** External-models endpoints, inference tables, and provisioned throughput may be limited. Every such limit is a documented ADR entry, not a blocker.
- **No investment advice.** The system produces grounded research answers with a disclaimer layer, never recommendations.
- **Snapshot data only.** Real-time pricing is out of scope.
- **Single tenant.** Multi-tenancy is explicitly out of scope.
- **Local numbers describe one device.** Where local hardware numbers appear, they describe a single machine. The eval discipline (fixed set, before and after, stated winner) is what transfers to another environment, not the raw figures.

## Scope drift

Log anything discovered during the build that changes the scope, and why. Rejection pattern #1 is skipping scoping, and scope drift is the honest record of what reality added.

| Date | Change | Why |
| --- | --- | --- |
| | | |
