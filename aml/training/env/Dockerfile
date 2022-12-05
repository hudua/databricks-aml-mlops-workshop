FROM mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04:20220902.v1

ENV AZUREML_CONDA_ENVIRONMENT_PATH /azureml-envs/sklearn-0.24.1
# Create conda environment
RUN conda create -p $AZUREML_CONDA_ENVIRONMENT_PATH \
    python=3.8.5

COPY statsmodels-0.13.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl /tmp/statsmodels-0.13.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# Prepend path to AzureML conda environment
ENV PATH $AZUREML_CONDA_ENVIRONMENT_PATH/bin:$PATH

# Install pip dependencies
RUN pip install 'scikit-learn==0.22.1'

RUN pip install /tmp/statsmodels-0.13.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

RUN pip install azureml-core
RUN pip install pandas
RUN pip install azureml-dataset-runtime
RUN pip install numpy

# This is needed for mpi to locate libpython
ENV LD_LIBRARY_PATH $AZUREML_CONDA_ENVIRONMENT_PATH/lib:$LD_LIBRARY_PATH
