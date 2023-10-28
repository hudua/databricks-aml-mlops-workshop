# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""
Trains ML model using training dataset. Saves trained model.
"""

import argparse

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

import mlflow
import mlflow.sklearn



def parse_args():
    '''Parse input arguments'''

    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_data", type=str, help="Path to raw data")
    parser.add_argument('--model_name', type=str, help='Name under which model will be registered')
    # parser.add_argument('--evaluation_output', type=str, help='Path of eval results')
    args = parser.parse_args()

    return args

def main(args):
    '''Read train dataset, train model, save trained model'''

    # Read train data
    df = pd.read_csv(Path(args.raw_data))

    # Split the data into input(X) and output(y)
    X = np.array(df[['humidity', 'temperature', 'windspeed']]).reshape(-1, 3)
    y = np.array(df['power']).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X,y)

    # log model hyperparameters
    mlflow.log_param("model", "LinearRegression")

    print("hubert is here!! Oct. 26 3:43PM")
    # Predict using the Regression Model
    yhat_train = model.predict(X)

    # Evaluate Regression performance with the train set
    r2 = r2_score(y, yhat_train)
    
    # log model performance metrics
    mlflow.log_metric("train r2", r2)

    mlflow.sklearn.log_model(model, args.model_name)

    # register logged model using mlflow
    run_id = mlflow.active_run().info.run_id
    model_uri = f'runs:/{run_id}/{args.model_name}'
    mlflow_model = mlflow.register_model(model_uri, args.model_name)

if __name__ == "__main__":
    
    mlflow.start_run()

    # ---------- Parse Arguments ----------- #
    # -------------------------------------- #

    args = parse_args()

    main(args)

    mlflow.end_run()
    
