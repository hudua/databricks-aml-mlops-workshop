# Databricks notebook source
# MAGIC %md Here is sample data from Databricks Delta table ```sensordata``` loaded

# COMMAND ----------

print('this is a live test at 3:33pm Wednesday')

# COMMAND ----------

# MAGIC %sql select * from sample.sensordata

# COMMAND ----------

# MAGIC %md As you can see, you can visualize it directly in Databricks. Now, let's run a simple correlation to see which numeric features correlate the most to ```power``` which is what we want to predict. We can introduce remote (local compute) using Azure Databricks Connect as well.

# COMMAND ----------

import pandas as pd
import os

try:
    if os.environ['REMOTECOMPUTE']=='True':
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()
except:
    pass

df = spark.sql('select * from sample.sensordata').toPandas()
print('Spark dataframe from Delta table queried')

# COMMAND ----------

df[['rpm','angle','temperature','humidity','windspeed','power']].corr()

# COMMAND ----------

# MAGIC %md For simplicity, let's just pick the column with the highest absolute correlation score so let's select ```humidity``` to predict ```power```

# COMMAND ----------

model_dataset = df[['humidity','power']]
print("Here is the correlation...", model_dataset.corr())

# COMMAND ----------

model_dataset.plot.scatter(x = 'humidity',y='power')

# COMMAND ----------

# MAGIC %md We will train a ```sklearn``` Linear Regression model and we will evaluate it based on a train/test split as well

# COMMAND ----------

train_test_split_ratio = 0.7

# COMMAND ----------

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

print("Now we train linear regression model based on train/test split")

eva_model = LinearRegression()
X = np.array(model_dataset['humidity']).reshape(-1, 1)
y = np.array(model_dataset['power']).reshape(-1, 1)

# COMMAND ----------

X_train, X_test, X_train, y_test = train_test_split(X, y, test_size = 1-train_test_split_ratio)

# COMMAND ----------

# MAGIC %md Now we can evaluate it based on the train test split

# COMMAND ----------

eva_model.fit(X_train, X_train)

# COMMAND ----------

# MAGIC %md Here is the ```abs_error``` which is the average absolute difference between the actual power and the predicted power

# COMMAND ----------

y_pred = eva_model.predict(X_test)
abs_error = np.mean(np.abs(y_pred - y_test))

# COMMAND ----------

print("Here is the absolute error", abs_error)

# COMMAND ----------

# MAGIC %md Now we can train the model on the entire data and register the model for operationalization

# COMMAND ----------

print("Now we train model on the entire dataset")

model = LinearRegression()
model.fit(X,y)

# COMMAND ----------

# MAGIC %md Now let's authenticate to Azure ML for model registry using user identity, and we can even leverage the mlflow APIs to track experiment results

# COMMAND ----------

from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.core import Workspace, Model, Experiment
import datetime
import mlflow

interactive_auth = InteractiveLoginAuthentication(tenant_id="<id>")
ws = Workspace(
        workspace_name="amlhudua",
        subscription_id =  "<sub-id>",
        resource_group = 'mlops'
    )
mlflow.set_tracking_uri(ws.get_mlflow_tracking_uri())

# COMMAND ----------

# MAGIC %md We set up ```mlflow``` tracking URI

# COMMAND ----------

experiment_name = 'mlops_end2end'
mlflow.set_experiment(experiment_name)

print("Now we use mlflow to track experiments")

with mlflow.start_run() as mlflow_run:
    mlflow.log_param("trainingdatetime", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    mlflow.log_metric("train_test_split", train_test_split_ratio)
    mlflow.log_metric("abs_error", abs_error)

# COMMAND ----------

# MAGIC %md Finally, we register the model in Azure ML

# COMMAND ----------

import pickle, os

print("Now we use Azure ML to register model in AML registry")
try:
    pickle.dump(model, open('/model.pkl', 'wb'))
    os.chdir('/')
except:
    pickle.dump(model, open('model.pkl', 'wb'))
model = Model.register(workspace = ws,
                       model_name="mlopsmodel",
                       model_path = "model.pkl",
                       description = 'Regression Model'
                      )
