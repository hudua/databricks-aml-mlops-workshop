# Databricks notebook source
# MAGIC %md This notebook creates a Databricks Delta table based on the file ```sample_data.csv```

# COMMAND ----------

# MAGIC %sql
# MAGIC create database if not exists sample

# COMMAND ----------

import pandas as pd
df = spark.createDataFrame(pd.DataFrame(pd.read_csv('/dbfs/mnt/data/sample_data.csv')))

# COMMAND ----------

df.write.format('delta').partitionBy('deviceid').mode("overwrite").save('/mnt/data/delta/sensordata')

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table if exists sample.sensordata;
# MAGIC CREATE TABLE sample.sensordata
# MAGIC USING DELTA
# MAGIC LOCATION '/mnt/data/delta/sensordata'

# COMMAND ----------

# MAGIC %sql select * from sample.sensordata
