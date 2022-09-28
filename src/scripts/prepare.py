import os
import click
from pandas import DataFrame
import pandas
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn
from decorators.load_path_context import PathLoadContext


@click.command(
    help="Prepare and split dataset in train and test."
    "The input is expected in parquet format."
)
@click.argument('environment_type', type=click.STRING)
@PathLoadContext()
def main(environment_type):
    # Todos os imports que estão dentro de src devem ser definidos aqui nesse escpo
    # Também obrigatório utilizar a função PathLoadContext()
    from src.core.enum.data_extraction_strategy_by_context_enum import StrategyByContextEnum
    
    strategy = StrategyByContextEnum[environment_type]
    wine_quality_dataset: DataFrame = pandas.read_parquet(f'{strategy.value().DATA_PATH}/wine_quality_raw.parquet.gzip')
    
    train, test = train_test_split(wine_quality_dataset, test_size=0.3)
    
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]
    
    train_x.to_parquet(os.path.join(strategy.value().DATA_PATH, 'train_x.parquet.gzip'), compression='gzip')
    test_x.to_parquet(os.path.join(strategy.value().DATA_PATH, 'test_x.parquet.gzip'), compression='gzip')
    train_y.to_parquet(os.path.join(strategy.value().DATA_PATH, 'train_y.parquet.gzip'), compression='gzip')
    test_y.to_parquet(os.path.join(strategy.value().DATA_PATH, 'test_y.parquet.gzip'), compression='gzip')
    
    with mlflow.start_run(run_name='PREP'):
        mlflow.log_artifact(os.path.join(strategy.value().DATA_PATH, 'train_x.parquet.gzip'), 'data')
        mlflow.log_artifact(os.path.join(strategy.value().DATA_PATH, 'test_x.parquet.gzip'), 'data')
        mlflow.log_artifact(os.path.join(strategy.value().DATA_PATH, 'train_y.parquet.gzip'), 'data')
        mlflow.log_artifact(os.path.join(strategy.value().DATA_PATH, 'test_y.parquet.gzip'), 'data')

if __name__ == "__main__":
    main()