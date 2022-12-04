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
import pickle
import numpy as np

subscription_id = ''
resource_group = ''
workspace_name = ''

ws = Workspace(subscription_id, resource_group, workspace_name)

dataset = Dataset.get_by_name(ws, name='mldata')

df = dataset.to_pandas_dataframe()

X = np.array(df[['humidity', 'temperature', 'windspeed']]).reshape(-1, 3)
y = np.array(df['power']).reshape(-1, 1)
```

You can first evaluate the model
```
from sklearn.model_selection import train_test_split
eva_model = LinearRegression()

X_train, X_test, Y_train, y_test = train_test_split(X, y, test_size = 0.3)

eva_model.fit(X_train, Y_train)

y_pred = eva_model.predict(X_test)
abs_error = np.mean(np.abs(y_pred - y_test))
print(abs_error)
```

Then you can track this experiment in Azure ML:


And finally you can then train the entire model and register the model
```
model = LinearRegression()

model.fit(X,y)

pickle.dump(model, open('./model.pkl', 'wb'))
model = Model.register(workspace = ws,
                       model_name="mlopsmodeltraining",
                       model_path = "./model.pkl",
                       description = 'Regression Model'
                      )
```
