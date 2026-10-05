# Databricks notebook source
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.sec_lab")  

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.finance")

# COMMAND ----------

spark.sql("SELECT 'setup ok'")