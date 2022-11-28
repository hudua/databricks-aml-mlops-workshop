# Databricks notebook source

# generally this should be done via the data lake, dfs, api but for the workshop we will just use the blob api

dbutils.fs.mount(
  source = "wasbs://data@<datalakename>.blob.core.windows.net",
  mount_point = "/mnt/data",
  extra_configs = {"fs.azure.account.key.<datalakename>.blob.core.windows.net":"<access-key>"})

# COMMAND ----------

# MAGIC %fs ls /mnt/data

# COMMAND ----------


