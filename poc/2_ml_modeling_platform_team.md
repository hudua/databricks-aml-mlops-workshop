Here are some code to do model training in Databricks:

```
import pandas as pd
df = spark.sql('select * from sample.sensordata').toPandas()
```

Then you can look for correlations
```
df[['rpm','angle','temperature','humidity','windspeed','power']].corr()
```

Say you want to see the correlation between humidity and power
```
model_dataset = df[['humidity','power']]
print("Here is the correlation...", model_dataset.corr())
```

```
model_dataset.plot.scatter(x = 'humidity',y='power')
```

Now we can train a model
```
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

print("Now we train linear regression model based on train/test split")

eva_model = LinearRegression()
X = np.array(model_dataset['humidity']).reshape(-1, 1)
y = np.array(model_dataset['power']).reshape(-1, 1)

train_test_split_ratio = 0.7
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1-train_test_split_ratio)
```

```
eva_model.fit(X_train, y_train)
```

Now we can get a model accuracy
```
y_pred = eva_model.predict(X_test)
abs_error = np.mean(np.abs(y_pred - y_test))
print("Here is the absolute error", abs_error)
```

