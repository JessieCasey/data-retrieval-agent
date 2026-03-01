import pandas as pd
import pytest

from data_retrieval_agent.sql_executor import (
    SQLValidationError,
    enforce_limit,
    execute_sql,
    validate_select_only,
)


def test_validate_select_only_rejects_non_select() -> None:
    with pytest.raises(SQLValidationError):
        validate_select_only("DELETE FROM records")


def test_enforce_limit_appends_when_missing() -> None:
    sql = "SELECT * FROM records"
    assert enforce_limit(sql, 10).endswith("LIMIT 10")


def test_enforce_limit_clamps_existing_limit() -> None:
    sql = "SELECT * FROM records LIMIT 100"
    assert enforce_limit(sql, 10) == "SELECT * FROM records LIMIT 10"


def test_execute_sql_returns_rows() -> None:
    dataframe = pd.DataFrame({"name": ["a", "b"], "value": [1, 2]})
    result = execute_sql(
        sql="SELECT name FROM records",
        dataframe=dataframe,
        table_name="records",
        max_limit=10,
    )
    assert list(result["name"]) == ["a", "b"]
