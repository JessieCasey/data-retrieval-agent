import re
from pathlib import Path

import pandas as pd
from pandasql import sqldf

from config import TABLE_NAME
from services.abstract.tabular_data_service import TabularDataService


class PandasExcelDataService(TabularDataService):
    def __init__(self) -> None:
        self.table_name = TABLE_NAME

    def load_excel(self, filename: Path) -> pd.DataFrame:
        if not filename.exists():
            raise FileNotFoundError(f"Excel file not found: {filename}")

        try:
            dataframe = pd.read_excel(filename)
        except Exception as exc:  # pragma: no cover - pandas/openpyxl errors vary.
            raise ValueError(f"Failed to read Excel file: {exc}") from exc

        if dataframe.empty:
            raise ValueError("The Excel file was loaded but contains no rows.")

        return dataframe

    def execute_sql(self, sql: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            result = sqldf(sql, {self.table_name: dataframe})
        except Exception as exc:  # pragma: no cover - pandasql/sqlite errors vary.
            fallback_sql = self._quote_unsafe_columns(sql, dataframe)
            if fallback_sql != sql:
                try:
                    result = sqldf(fallback_sql, {self.table_name: dataframe})
                except Exception as fallback_exc:  # pragma: no cover
                    raise ValueError(
                        f"Failed to execute pandasql query: {fallback_exc}"
                    ) from fallback_exc
            else:
                raise ValueError(f"Failed to execute pandasql query: {exc}") from exc

        if not isinstance(result, pd.DataFrame):
            raise ValueError("pandasql returned unexpected result type.")

        return result

    def _quote_unsafe_columns(self, sql: str, dataframe: pd.DataFrame) -> str:
        updated_sql = sql
        for column in sorted((str(col) for col in dataframe.columns), key=len, reverse=True):
            if self._is_safe_identifier(column):
                continue

            quoted_column = self._quote_identifier(column)
            pattern = re.compile(rf'(?<!")({re.escape(column)})(?!")')
            updated_sql = pattern.sub(quoted_column, updated_sql)
        return updated_sql

    def _is_safe_identifier(self, identifier: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", identifier))

    def _quote_identifier(self, identifier: str) -> str:
        escaped = identifier.replace('"', '""')
        return f'"{escaped}"'
