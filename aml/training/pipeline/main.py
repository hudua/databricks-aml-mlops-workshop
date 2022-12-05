from azureml.core import Workspace, Dataset, Datastore, Experiment, Environment
from azureml.core.compute import AmlCompute
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import PipelineParameter, StepSequence, Pipeline

subscription_id = ''
resource_group = ''
workspace_name = ''

ws = Workspace(subscription_id, resource_group, workspace_name)

aml_compute = AmlCompute(ws, "testcluster")

env = Environment('New_env_name')

env.docker.base_image = '.azurecr.io/repo/train-env:v1'
env.python.user_managed_dependencies = True

# create a new runconfig object
run_config = RunConfiguration()
run_config.environment = env

run_step = PythonScriptStep(script_name="main_script.py",
                            compute_target=aml_compute,
                            source_directory='program',
                            runconfig = run_config,
                            allow_reuse = False)

steps = StepSequence(steps = [run_step])
pipeline = Pipeline(workspace=ws, steps=steps)
pipeline.validate()

Experiment(ws, "PIPELINE_MAIN_Run").submit(pipeline, regenerate_outputs=True)
