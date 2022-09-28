import click

import mlflow
import mlflow.sklearn

@click.command()
@click.argument('environment_type', type=click.STRING)
def main(environment_type):
    with mlflow.start_run():
        mlflow.run(uri='.', entry_point='extract', parameters={'environment_type': environment_type})
        
        mlflow.run(uri='.', entry_point='prepare', parameters={'environment_type': environment_type})
        
        train_run = mlflow.run(uri='.', entry_point='train', parameters={'environment_type': environment_type})

        mlflow.run(uri='.', entry_point='validate', parameters={'environment_type': environment_type, 'train_run_id': train_run.run_id})

        mlflow.run(uri='.', entry_point='model_registry', parameters={'train_run_id': train_run.run_id})
        
if __name__ == '__main__':
    main()