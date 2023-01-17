# Databricks notebook source

# generally this should be done via the data lake, dfs, api but for the workshop we will just use the blob api

dbutils.fs.mount(
  source = "wasbs://data@<datalakename>.blob.core.windows.net",
  mount_point = "/mnt/data",
  extra_configs = {"fs.azure.account.key.<datalakename>.blob.core.windows.net":"<access-key>"})

# COMMAND ----------

# MAGIC %fs ls /mnt/data

# COMMAND ----------

secret = dbutils.secrets.get(scope = 'kv', key = 'dlmountsp')
configs = {"fs.azure.account.auth.type": "OAuth",
       "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
       "fs.azure.account.oauth2.client.id": "<app (client) id>",
       "fs.azure.account.oauth2.client.secret": secret,
       "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<tenant-id>/oauth2/token",
       "fs.azure.createRemoteFileSystemDuringInitialization": "true"}

dbutils.fs.mount(
source = "abfss://<container-name>@<storage-name>.dfs.core.windows.net",
mount_point = "/mnt/rawdfs",
extra_configs = configs)

