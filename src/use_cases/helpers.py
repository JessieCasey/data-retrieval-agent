import pandas as pd

MAX_PREVIEW_ROWS = 10


def build_result_preview(
    dataframe: pd.DataFrame,
) -> tuple[list[str], list[list[str]], bool]:
    preview_dataframe = dataframe.head(MAX_PREVIEW_ROWS)
    preview_columns = [str(column) for column in preview_dataframe.columns]
    preview_rows = [
        [format_cell(value) for value in row]
        for row in preview_dataframe.itertuples(index=False, name=None)
    ]
    preview_truncated = len(dataframe.index) > MAX_PREVIEW_ROWS
    return preview_columns, preview_rows, preview_truncated


def format_cell(value: object) -> str:
    if pd.isna(value):
        return "NULL"
    if isinstance(value, pd.Timestamp):
        return value.isoformat(sep=" ")
    return str(value)
