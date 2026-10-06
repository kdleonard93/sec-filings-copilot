# Databricks notebook source
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.sec_lab")  

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.finance")

# COMMAND ----------

spark.sql("SELECT 'setup ok'")

# COMMAND ----------

# MAGIC %pip install pypdf beautifulsoup4

# COMMAND ----------

import sys, os
LIB = "/Workspace/Users/<you>/sec-filings-copilot/notebooks/lib"
if LIB not in sys.path:
    sys.path.append(LIB)
import parsing

RAW = "/Volumes/workspace/sec_lab/raw"
docs, seen, dedupe_log = [], {}, []
for name in sorted(os.listdir(RAW)):
    if not name.lower().endswith((".html", ".htm", ".pdf")):
        continue
    text = parsing.clean(parsing.extract(os.path.join(RAW, name)))
    h = parsing.content_hash(text)
    if h in seen:                       # same content already ingested
        dedupe_log.append((name, seen[h])); continue
    seen[h] = name
    docs.append((name, text))           # list of (source, text) for Step 3
print(f"{len(docs)} unique docs, {sum(len(t) for _, t in docs):,} chars")
print("duplicates skipped:", dedupe_log)