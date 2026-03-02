from abc import abstractmethod

import pandas as pd


class LlmQueryService:
    @abstractmethod
    def generate_sql(self, prompt: str, dataframe: pd.DataFrame) -> str:
        raise NotImplementedError

    @abstractmethod
    def summarize_query_result(
        self,
        prompt: str,
        generated_sql: str,
        query_dataframe: pd.DataFrame,
    ) -> str:
        raise NotImplementedError
