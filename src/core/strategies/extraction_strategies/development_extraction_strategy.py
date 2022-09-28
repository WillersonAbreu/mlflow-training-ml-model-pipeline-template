import os
import pandas
from pandas import DataFrame
from src.core.strategies.extraction_strategies.abstract_extraction_strategy import AbstractExtractionStrategy


class DevelopmentExtractionStrategy(AbstractExtractionStrategy):
    DATA_PATH = os.path.realpath(
        os.path.join(
            os.getcwd(),
            os.path.dirname(__file__),
            '..',
            '..',
            '..',
            '..',
            'temp',
            'dataset'
        ) 
    )
    
    def load_data(self) -> DataFrame:
        return pandas.read_parquet(f'{self.DATA_PATH}/wine_quality.parquet.gzip')