# databricks-aml-mlops-workshop

#### Step 1: Data lake structure
Set-up common data lake structure to
* ```raw```: this is where you can upload the sample sensor CSV file
* ```delta```: this is where you save the delta tables
* ```curated```: this is where you can save the ML-ready and ML-predictions datasets

#### Step 2: Databricks
Create a Databricks cluster with runtime ```10.4 LTS (includes Apache Spark 3.2.1, Scala 2.12)``` and ensure that these two libraries are installed:
* ```azureml-core```
* ```azureml-mlflow```

You will want to create a mount point from Databricks to the data lake using the ```utils/mount.py``` example using access key for blob storage option (simplest option without any other dependencies).

You will also want to set up Repo integration with Azure Repos and Databricks Repos: https://learn.microsoft.com/en-us/azure/databricks/repos/repos-setup

#### Step 3: Spark analysis
Run the delta table and feature engineering / modeling scripts to
* Create delta table and enable SQL-queries
* Run feature engineering and modeling
* Register model with Azure ML and mlflow

#### Step 4: Azure DevOps
See the example DevOps pipeline for how to create a model training and model deployment pipeline. Here is a really good example for using the Databricks APIs: https://github.com/crflynn/databricks-api
