With the ML-ready dataset saved in the ```curated``` zone of the data lake, you are now ready for ML modeling.

Go to Azure ML and create a dataset referencing this data:
* Go to Data and then the Datastores tab
* Click on create and enter the necessary info. You will need the access key from the storage account
* Enable workspace managed identity for data previewing
* Now click on the newly created datastore and click on create data asset
* Give it a name and under Type, please select Tabular from Azure ML v1 APIs
* Browse and pick the ml ready dataset saved from Azure Databricks
* You should be able to preview it and can verify
* Create the dataset

Now, please proceed for model training using three ways:
* Through a notebook (Python code approach), and of course can try VS Code option as well. Please connect to Azure ML directly, without VPN
* Automated ML (no-code)
* Designer (drag-and-drop)

For Automated ML and Designer, first go to Compute and create a compute cluster
