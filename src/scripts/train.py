import os
import click
import pandas as pd
from sklearn.linear_model import ElasticNet
import mlflow
import mlflow.sklearn
from decorators.load_path_context import PathLoadContext

@click.command(
    help="Trains an Keras model on wine_quality dataset."
    "The input is expected in parquet format."
    "The model are logged with mlflow."
)
@click.argument('environment_type', type=click.STRING)
def main(environment_type):

    with mlflow.start_run(), PathLoadContext():
        # Todos os imports que estão dentro de src devem ser definidos aqui nesse escpo
        # Também obrigatório utilizar a função PathLoadContext()
        from src.core.contexts.extract_context.data_extraction_by_environment import DataExtractionByEnvironment
        from src.core.enum.data_extraction_strategy_by_context_enum import AbstractExtractionStrategy, StrategyByContextEnum
        from src.core.strategies.extraction_strategies.abstract_extraction_strategy import AbstractExtractionStrategy
        
        strategy = StrategyByContextEnum[environment_type]
        
        mlflow.log_param("model", 'Elasticnet')
        mlflow.log_param("alpha", 0.1)
        mlflow.log_param("l1_ratio", 0.1)

        train_x = pd.read_parquet(os.path.join(strategy.value().DATA_PATH, 'train_x.parquet.gzip'))
        
        train_y = pd.read_parquet(os.path.join(strategy.value().DATA_PATH, 'train_y.parquet.gzip'))
        
        lr = ElasticNet(alpha=0.1, l1_ratio=0.1, random_state=42)
        lr.fit(train_x, train_y)
        
        mlflow.sklearn.log_model(lr, "model")

if __name__ == "__main__":
    main()