# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# dependencies = [
#   "langchain-text-splitters",
# ]
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

notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
search_directory = "/Workspace" + notebook_path
library_directory = None
while True:
    candidate_directory = os.path.join(search_directory, "notebooks", "lib")
    if os.path.isdir(candidate_directory):
        library_directory = candidate_directory
        break
    parent_directory = os.path.dirname(search_directory)
    if parent_directory == search_directory:
        break
    search_directory = parent_directory
if library_directory is None:
    raise FileNotFoundError(f"no notebooks/lib above {notebook_path} - create parsing.py there and push/pull it")
if library_directory not in sys.path:
    sys.path.append(library_directory)
import parsing
print("parsing loaded from", parsing.__file__)

raw_directory = "/Volumes/workspace/sec_lab/raw"
documents, seen_content_hashes, duplicate_log = [], {}, []
for file_name in sorted(os.listdir(raw_directory)):
    if not file_name.lower().endswith((".html", ".htm", ".pdf")):
        continue
    document_text = parsing.clean(parsing.extract(os.path.join(raw_directory, file_name)))
    content_digest = parsing.content_hash(document_text)
    if content_digest in seen_content_hashes:
        duplicate_log.append((file_name, seen_content_hashes[content_digest]))
        continue
    seen_content_hashes[content_digest] = file_name
    documents.append((file_name, document_text))
print(f"{len(documents)} unique documents, {sum(len(document_text) for _, document_text in documents):,} chars")
print("duplicates skipped:", duplicate_log)

# COMMAND ----------

# MAGIC %pip install langchain-text-splitters

# COMMAND ----------

from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid, re
from datetime import date
from pathlib import Path

text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)

def recursive_chunks(documents):
    chunks = []
    for source_file_name, document_text in documents:
        for chunk_text in text_splitter.split_text(document_text):
            if chunk_text.strip():
                chunks.append((source_file_name, chunk_text.strip()))
    return chunks

def table_aware_chunks(documents):
    chunks = []
    for source_file_name, document_text in documents:
        for block in split_into_blocks(document_text):
            if is_table(block):
                chunks.append((source_file_name, block))
            else:
                chunks.extend((source_file_name, chunk_text) for chunk_text in text_splitter.split_text(block))
    return chunks

source_directory = "/Volumes/workspace/sec_lab/raw"

def parse_file_name(source_file_name):
    ticker, form, period = (Path(source_file_name).stem.split("_") + ["", ""])[:3]
    year_match = re.search(r"\d{4}", period)
    return {"ticker": ticker, "form": form,
            "fiscal_year": int(year_match.group()) if year_match else None}

def chunks_to_rows(chunk_list):
    rows = []
    for source_file_name, chunk_text in chunk_list:
        rows.append({"chunk_id": str(uuid.uuid4()), "content": chunk_text, "source": source_file_name,
                     "source_uri": f"{source_directory}/{source_file_name}", "retrieved_at": date.today().isoformat(),
                     **parse_file_name(source_file_name)})
    return rows

spark.createDataFrame(chunks_to_rows(recursive_chunks(documents))).write.mode("overwrite") \
  .option("overwriteSchema", "true").saveAsTable("workspace.sec_lab.chunks_v1")
spark.createDataFrame(chunks_to_rows(table_aware_chunks(documents))).write.mode("overwrite") \
  .option("overwriteSchema", "true").saveAsTable("workspace.sec_lab.chunks_v2")