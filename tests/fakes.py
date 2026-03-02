from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from services.abstract.llm_query_service import LlmQueryService
from services.abstract.tabular_data_service import TabularDataService


@dataclass
class MockTabularDataService(TabularDataService):
    loaded_dataframe: pd.DataFrame = field(
        default_factory=lambda: pd.DataFrame({"customer_id": [1, 2, 3]}),
    )
    query_result_dataframe: pd.DataFrame = field(
        default_factory=lambda: pd.DataFrame({"total_customers": [3]}),
    )

    def load_excel(self, filename: Path) -> pd.DataFrame:
        _ = filename
        return self.loaded_dataframe

    def execute_sql(self, sql: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        _ = sql
        _ = dataframe
        return self.query_result_dataframe


@dataclass
class MockLlmQueryService(LlmQueryService):
    sql: str = "SELECT COUNT(*) AS total_customers FROM records"
    summary: str = "There are 3 customers."

    def generate_sql(self, prompt: str, dataframe: pd.DataFrame) -> str:
        _ = prompt
        _ = dataframe
        return self.sql

    def summarize_query_result(
        self,
        prompt: str,
        generated_sql: str,
        query_dataframe: pd.DataFrame,
    ) -> str:
        _ = prompt
        _ = generated_sql
        _ = query_dataframe
        return self.summary


class FailingTabularDataService(TabularDataService):
    def __init__(self, message: str = "Missing file") -> None:
        self.message = message

    def load_excel(self, filename: Path) -> pd.DataFrame:
        raise FileNotFoundError(f"{self.message}: {filename}")

    def execute_sql(self, sql: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        _ = sql
        _ = dataframe
        raise RuntimeError("Should not be called")
