import click
import mlflow
from pandas import DataFrame
from decorators.load_path_context import PathLoadContext


@click.command()
@click.argument('environment_type', type=click.STRING)
def extract_data(environment_type: str):    
    with mlflow.start_run(), PathLoadContext():
        # Todos os imports que estão dentro de src devem ser definidos aqui nesse escpo
        # Também obrigatório utilizar a função PathLoadContext()
        from src.core.contexts.extract_context.data_extraction_by_environment import DataExtractionByEnvironment
        from src.core.enum.data_extraction_strategy_by_context_enum import AbstractExtractionStrategy, StrategyByContextEnum
        from src.core.strategies.extraction_strategies.abstract_extraction_strategy import AbstractExtractionStrategy
        
        print('Launching extraction')
        strategy = StrategyByContextEnum[environment_type]
        context: AbstractExtractionStrategy = DataExtractionByEnvironment(strategy.get_current_strategy())
        wine_quality: DataFrame = context.load_data()

        print('Printing dataset: ')
        print(wine_quality.head(1))

        wine_quality_dataset = f'{strategy.value().DATA_PATH}/wine_quality_raw.parquet.gzip'
        
        print(f'Saving parquet into {wine_quality_dataset} path')
        wine_quality.to_parquet(wine_quality_dataset, compression='gzip')
        mlflow.log_artifact(wine_quality_dataset, 'data')

if __name__ == '__main__':
    extract_data()