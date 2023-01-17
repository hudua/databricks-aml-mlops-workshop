# will need Storage Blob Data Contributor role for Data Lake to access

dbutils.fs.ls("abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<path-to-data>")


df = spark.read.csv("abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<path-to-data>",inferSchema=True, header=True)
