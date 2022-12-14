To operationalize, let's first set up the training environment. In your Azure ML terminal, run a 

```
git clone https://github.com/hudua/databricks-aml-mlops-workshop.git
```

Then go to this directory in the terminal: ```cd databricks-aml-mlops-workshop/aml/training/env```.

Then run these two commands:

```
docker build -t amlacrhudua.azurecr.io/repo/train-env:v1 .
az acr login -n amlacrhudua
docker push amlacrhudua.azurecr.io/repo/train-env:v1
```
You can find the admin login and password in Azure Container Registry in Azure Portal.

Once this is done, go to ```cd ../pipeline``` and you can edit the main.py file. Please update the subscription ID, resource group, workspace name, the compute cluster name, and the container registry name.

Then simply run ```python main.py``` for automated model training.

For model deployment, let's set up the deployment environment. Go to the deployment folder using ```cd ../../deployment/env```.

Then run these two commands:

```
docker build -t amlacrhudua.azurecr.io/repo/deploy-env:v1 .
az acr login -n amlacrhudua
docker push amlacrhudua.azurecr.io/repo/deploy-env:v1
```

Now go to ```cd/..``` and edit the ```endpoint.yml``` and ```deployment.yml``` files so the endpoint name is unique. Then run
```
az login
az extension add -n ml
az account set -s "Workload1"
az configure --defaults workspace=amlhudua group=mlops
az ml online-endpoint create  -f endpoint.yml
az ml online-deployment create  -f deployment.yml

```
