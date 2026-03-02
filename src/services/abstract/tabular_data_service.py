from abc import abstractmethod
from pathlib import Path

import pandas as pd


class TabularDataService:
    @abstractmethod
    def load_excel(self, filename: Path) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def execute_sql(self, sql: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError
