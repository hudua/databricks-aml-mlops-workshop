import azure.functions as func
import datetime
import json
import logging
import pandas as pd
import urllib.request
import pandas as pd
from io import BytesIO
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

@app.route(route="HttpExample", auth_level=func.AuthLevel.FUNCTION)
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    data = req.get_json()
    logging.info(data['data'])
    df_live = pd.DataFrame({"date":[data['data']['date'][0]],"column1":[data['data']['column2'][0]]})
    df_live['date'] = df_live['date'].astype(str)
    logging.info(df_live)
    CONNECTION_STRING=""
    CONTAINERNAME="silver"
    BLOBNAME="pre-calculated_data_daily.csv"

    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINERNAME)
    blob_client = container_client.get_blob_client(BLOBNAME)

    with BytesIO() as input_blob:
        blob_client.download_blob().download_to_stream(input_blob)
        input_blob.seek(0)
        df_pre = pd.read_csv(input_blob, index_col=False)
    df_pre['date'] = df_pre['date'].astype(str)

    df_full = df_live.merge(df_pre, on='date')
    logging.info(df_full)
    data = {"data":[df_full.iloc[0,1],df_full.iloc[0,3]]}

    body = str.encode(json.dumps(data))

    url = 'https://.canadacentral.inference.ml.azure.com/score'

    api_key = ''

    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'mlopsmodel-1' }

    req = urllib.request.Request(url, body, headers)

    response = urllib.request.urlopen(req)

    result = response.read()
    result = json.loads(result)
    predict = ''
    if result[0][0] > 45:
        predict = "Green"
    else:
        predict = "Grey"
    return func.HttpResponse(
             f"Prediction is {predict} and regression score is {result[0][0]}.",
             status_code=200
        )
