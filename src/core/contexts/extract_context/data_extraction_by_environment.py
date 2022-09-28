from pandas import DataFrame

from src.core.strategies.extraction_strategies.abstract_extraction_strategy import AbstractExtractionStrategy

class DataExtractionByEnvironment:
    def __init__(self, current_strategy: AbstractExtractionStrategy) -> None:
        self._extraction_strategy = current_strategy
        
    @property
    def strategy(self) -> AbstractExtractionStrategy:
        return self._extraction_strategy
    
    @strategy.setter
    def set_strategy(self, current_strategy: AbstractExtractionStrategy) -> None:
        self._extraction_strategy = current_strategy
        
    def load_data(self) -> DataFrame:
        return self._extraction_strategy.load_data()
