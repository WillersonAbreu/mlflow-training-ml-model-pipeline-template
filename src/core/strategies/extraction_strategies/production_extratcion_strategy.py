
import os

from pandas import DataFrame
import pandas
from src.core.strategies.extraction_strategies.abstract_extraction_strategy import AbstractExtractionStrategy
from src.core.services.wine_quality_extract_service import DATA_PATH, get_dataset


class ProductionExtractionStrategy(AbstractExtractionStrategy):
    DATA_PATH = os.path.join(
        os.getcwd(),
        os.path.dirname(__file__),
        '..',
        '..',
        '..',
        '..',
        'temp',
        'dataset'
    )
    
    # TODO: Baixar do github
    def load_data(self) -> DataFrame:
        get_dataset()
        df = pandas.read_csv(os.path.join(DATA_PATH))
        return df
        
