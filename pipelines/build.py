import mlflow
import sys
import mlflow.azureml
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication

if __name__ == "__main__":

    tenantId = sys.argv[1]
    principalId = sys.argv[2]
    principalPass = sys.argv[3]
    workspaceName = sys.argv[4]
    subscriptionId = sys.argv[5]
    resourceGroup = sys.argv[6]
    
    sp = ServicePrincipalAuthentication(
        tenant_id=tenantId,
        service_principal_id=principalId,
        service_principal_password=principalPass
    )

    ws = Workspace.get(
        name=workspaceName,
        auth=sp,
        subscription_id=subscriptionId,
        resource_group=resourceGroup
    )


    mlflow.set_tracking_uri(ws.get_mlflow_tracking_uri())

    experiment_name = "template-wine-quality"
    mlflow.set_experiment(experiment_name)

    backend_config = {"COMPUTE": "S-DS3-v2", "USE_CONDA": False}

    remote_mlflow_run=  mlflow.projects.run(uri="../.", 
                                    backend = "azureml",
                                    backend_config = backend_config,
                                    synchronous=True)

    run_job_id = remote_mlflow_run.run_id

    run = mlflow.get_run(run_job_id)
    
    if run.info.status == 'FINISHED':
        print(run_job_id)