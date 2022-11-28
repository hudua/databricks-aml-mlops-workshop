import sys
from databricks_api import DatabricksAPI

token = sys.argv[1]

db = DatabricksAPI(
    host="https://adb-<id>.<n>.azuredatabricks.net/",
    token=token
)

db.repos.update_repo(
    id = <id>,
    branch='main'
)

db.jobs.run_now(
    job_id=<id> 
)
