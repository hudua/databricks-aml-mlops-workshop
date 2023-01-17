You can download the dataset here: https://storagepublicfreestuff.blob.core.windows.net/esdc/sample_data.csv

Here's how you can create a Delta table

```
df = spark.read.csv("abfss://raw@msfthuduadevdl.dfs.core.windows.net/sample_data.csv",inferSchema=True, header=True)
df.write.format('delta').partitionBy('deviceid').mode("overwrite").save('/mnt/raw/delta/sensordata')
```

Then convert to writing SQL in the same notebook

```
%sql
create database if not exists sample
```

```
%sql
drop table if exists sample.sensordata;
CREATE TABLE sample.sensordata
USING DELTA
LOCATION '/mnt/raw/delta/sensordata'
```

And here is sample code for model training: https://storagepublicfreestuff.blob.core.windows.net/esdc/model-training.html
