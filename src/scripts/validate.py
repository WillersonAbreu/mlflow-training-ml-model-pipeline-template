import os
import click
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mlflow
import mlflow.sklearn

from decorators.load_path_context import PathLoadContext


@click.command(
    help="Evaluate an Keras model."
    "The inputs is expected in parquet format."
    "The metrics are logged with mlflow."
)
@click.argument('environment_type', type=click.STRING)
@click.argument('train_run_id', type=click.STRING)
def main(environment_type: str, train_run_id: str):
    with mlflow.start_run(), PathLoadContext():
        # Todos os imports que estão dentro de src devem ser definidos aqui nesse escpo
        # Também obrigatório utilizar a função PathLoadContext()
        from src.core.contexts.extract_context.data_extraction_by_environment import DataExtractionByEnvironment
        from src.core.enum.data_extraction_strategy_by_context_enum import AbstractExtractionStrategy, StrategyByContextEnum
        from src.core.strategies.extraction_strategies.abstract_extraction_strategy import AbstractExtractionStrategy
            
        strategy = StrategyByContextEnum[environment_type]
        
        test_x = pd.read_parquet(os.path.join(strategy.value().DATA_PATH, 'test_x.parquet.gzip'))
        test_y = pd.read_parquet(os.path.join(strategy.value().DATA_PATH, 'test_y.parquet.gzip'))

        model_uri = f'runs:/{train_run_id}/model'
        
        lr = mlflow.sklearn.load_model(model_uri=model_uri)
 
        predicted_qualities = lr.predict(test_x)

        rmse = np.sqrt(mean_squared_error(test_y, predicted_qualities))
        mae = mean_absolute_error(test_y, predicted_qualities)
        r2 = r2_score(test_y, predicted_qualities)

        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        assert mae <= 0.7
        assert rmse <= 0.8
        assert r2 <= 0.3

if __name__ == "__main__":
    main()