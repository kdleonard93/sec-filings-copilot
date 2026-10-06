# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.sec_lab")  

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.finance")

# COMMAND ----------

spark.sql("SELECT 'setup ok'")

# COMMAND ----------

# MAGIC %pip install pypdf beautifulsoup4

# COMMAND ----------

import sys, os

# find the repo's notebooks/lib from this notebook's own path (works in subfolders too)
nb = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
probe, LIB = "/Workspace" + nb, None
while True:
    cand = os.path.join(probe, "notebooks", "lib")
    if os.path.isdir(cand):
        LIB = cand; break
    parent = os.path.dirname(probe)
    if parent == probe:
        break
    probe = parent
if LIB is None:
    raise FileNotFoundError(f"no notebooks/lib above {nb} - create parsing.py there and push/pull it")
if LIB not in sys.path:
    sys.path.append(LIB)
import parsing
print("parsing loaded from", parsing.__file__)

RAW = "/Volumes/workspace/sec_lab/raw"
docs, seen, dedupe_log = [], {}, []
for name in sorted(os.listdir(RAW)):
    if not name.lower().endswith((".html", ".htm", ".pdf")):
        continue
    text = parsing.clean(parsing.extract(os.path.join(RAW, name)))
    h = parsing.content_hash(text)
    if h in seen:
        dedupe_log.append((name, seen[h])); continue
    seen[h] = name
    docs.append((name, text))
print(f"{len(docs)} unique docs, {sum(len(t) for _, t in docs):,} chars")
print("duplicates skipped:", dedupe_log)