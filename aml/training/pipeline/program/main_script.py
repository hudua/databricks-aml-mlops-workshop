from azureml.core import Workspace, Datastore, Dataset, Model, Run
import pandas as pd
import pickle
from testmethods import add
import statsmodels
import numpy as np

print('version of statsmodels is', statsmodels.__version__)

run = Run.get_context(allow_offline=True)
ws = run.experiment.workspace

dataset = Dataset.get_by_name(ws, name='mldata')
x = add.add_example_weird(2, 34)
print("custom module has a weird add method where add(2, 34) equals", x)

df = dataset.to_pandas_dataframe()
from sklearn.linear_model import LinearRegression

X = np.array(df[['humidity', 'temperature', 'windspeed']]).reshape(-1, 3)
y = np.array(df['power']).reshape(-1, 1)
model = LinearRegression()
model.fit(X,y)

pickle.dump(model, open('./model.pkl', 'wb'))
model = Model.register(workspace = ws,
                       model_name="mlopsmodeltraining",
                       model_path = "./model.pkl",
                       description = 'Regression Model'
                      )
