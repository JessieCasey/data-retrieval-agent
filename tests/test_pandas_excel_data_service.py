import pandas as pd

from services.pandas_excel_data_service import PandasExcelDataService


def test_execute_sql_quotes() -> None:
    dataframe = pd.DataFrame({"Orders": [1, 2, 4, 5]})
    service = PandasExcelDataService()

    result = service.execute_sql(
        "SELECT COUNT(DISTINCT Orders) AS total_customers FROM records",
        dataframe,
    )

    assert int(result.iloc[0]["total_customers"]) == 4


def test_execute_sql_quotes_unsafe_columns_on_retry() -> None:
    dataframe = pd.DataFrame({"Unnamed: 0": [1, 2, 2]})
    service = PandasExcelDataService()

    result = service.execute_sql(
        "SELECT COUNT(DISTINCT Unnamed: 0) AS total_customers FROM records",
        dataframe,
    )

    assert int(result.iloc[0]["total_customers"]) == 2
