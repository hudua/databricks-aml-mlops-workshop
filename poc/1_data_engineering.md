As you start the project, you find out there are two main datasets:

* The team has provided you with a starting dataset that collects power generation data, downloadable here: https://amlhudua1207855224.blob.core.windows.net/raw/power_gen_data.csv
* You can also retrieve weather data here: https://amlhudua1207855224.blob.core.windows.net/raw/weather_data.csv

As the first step of the PoC, you can upload these two datasets in the ```raw``` zone of your data lake.

Then you can use Azure Databricks to connect to these CSV files using the established mount point and create delta tables. Here is a quick code snippet:

```
df_power = pd.read_csv('/dbfs/mnt/raw/power_gen_data.csv')
spark_df_power = spark.createDataFrame(df_power)
spark_df_power.write.format('delta').partitionBy('deviceid').mode("overwrite").save('/mnt/delta/power_gen_data')

%sql
drop table if exists sample.power_gen_data;
CREATE TABLE sample.power_gen_data
USING DELTA
LOCATION '/mnt/delta/power_gen_data'

```

Please do the same for the weather data and now you should have two tables ```power_gen_data``` and ```weather_data```.
