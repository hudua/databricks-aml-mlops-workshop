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

For the notebook version, this code should run in Azure ML Notebook:

```
from sklearn.linear_model import LinearRegression
from azureml.core import Workspace, Dataset, Model

subscription_id = '7f7e7d61-990c-46bc-9dfd-4d6115ef04f6'
resource_group = 'mlops'
workspace_name = 'amlhudua'

ws = Workspace(subscription_id, resource_group, workspace_name,auth=msi_auth)

dataset = Dataset.get_by_name(ws, name='mldata')

df = dataset.to_pandas_dataframe()

X = np.array(df['humidity']).reshape(-1, 1)
y = np.array(df['power']).reshape(-1, 1)
model = LinearRegression()

model.fit(X,y)

pickle.dump(model, open('./model.pkl', 'wb'))
model = Model.register(workspace = ws,
                       model_name="mlopsmodeltraining",
                       model_path = "./model.pkl",
                       description = 'Regression Model'
                      )
```
