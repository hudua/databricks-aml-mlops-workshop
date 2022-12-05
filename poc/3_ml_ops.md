To operationalize, let's first set up the training environment. In your Azure ML terminal, run a 

```
git clone https://github.com/hudua/databricks-aml-mlops-workshop.git
```

Then go to this directory in the terminal: ```cd databricks-aml-mlops-workshop/aml/training/env```.

Then run these two commands:

```
docker build -t amlacrhudua.azurecr.io/repo/train-env:v1 .
docker push amlacrhudua.azurecr.io/repo/train-env:v1
```
