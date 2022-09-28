from os import getenv
import click
from dotenv import load_dotenv
import mlflow
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication

@click.command()
@click.argument("train_run_id", type=click.STRING)
def registry(train_run_id: str):
    print("Launching 'model_registry'")

    print('''
        IMPORTANTE!!!
        É necessário tirar os comentários de todos os do trecho dentro do script para que o registro do modelo seja efetivado.
        E o registro só vai acontecer se você rodar o script pipelines/build.py ou executando através de uma DAG 
        que dispara o treinamento no Azure ML.
    ''')
    
    # experiment_name = 'template-wine-quality'
    # mlflow.set_experiment(experiment_name)
    # model_uri="runs:/{}/model".format(train_run_id)
    # mlflow.register_model(model_uri, experiment_name)
    
if __name__ == '__main__':
    load_dotenv()
    registry()