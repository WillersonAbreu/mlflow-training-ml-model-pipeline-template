from enum import Enum

from src.core.strategies.extraction_strategies.abstract_extraction_strategy import AbstractExtractionStrategy
from src.core.strategies.extraction_strategies.development_extraction_strategy import DevelopmentExtractionStrategy
from src.core.strategies.extraction_strategies.production_extratcion_strategy import ProductionExtractionStrategy
from src.core.strategies.extraction_strategies.test_extraction_strategy import TestExtractionStrateg


class StrategyByContextEnum(Enum):
    TEST: AbstractExtractionStrategy = TestExtractionStrateg
    DEVELOPMENT: AbstractExtractionStrategy = DevelopmentExtractionStrategy
    PRODUCTION: AbstractExtractionStrategy = ProductionExtractionStrategy

    def get_current_strategy(self) -> AbstractExtractionStrategy:
        environment_strategy: AbstractExtractionStrategy = self.value()
        return environment_strategy