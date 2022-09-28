from abc import ABC
from pandas import DataFrame


class AbstractExtractionStrategy(ABC):
    
    @classmethod
    def load_data(self) -> DataFrame:
        pass  # Método abstrato, não necessita de implementação