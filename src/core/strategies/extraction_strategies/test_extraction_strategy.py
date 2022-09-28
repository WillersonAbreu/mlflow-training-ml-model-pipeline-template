import os

from pandas import DataFrame
import pandas
from src.core.strategies.extraction_strategies.abstract_extraction_strategy import AbstractExtractionStrategy


class TestExtractionStrateg(AbstractExtractionStrategy):
    DATA_PATH = os.path.realpath(
        os.path.join(
            os.getcwd(),
            os.path.dirname(__file__),
            '..',
            '..',
            '..',
            'tests',
            'dataset'
        )
    )
    
    def load_data(self) -> DataFrame:
        return pandas.read_parquet(f'{self.DATA_PATH}/wine_quality.parquet.gzip')