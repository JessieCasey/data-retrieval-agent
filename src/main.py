from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from services.openai_pandasql_service import OpenAIPandasqlService
from services.pandas_excel_data_service import PandasExcelDataService
from use_cases.ai_extraction_pipeline_query_use_case import (
    AiExtractionPipelineQueryUseCase,
)
from use_cases.decorators.error_handler import UseCaseExceptionResponse
from use_cases.request_models.ai_extraction_pipeline_query_request_model import (
    AiExtractionPipelineQueryRequestModel,
)

app = typer.Typer(help="data-retrieval-agent CLI", add_completion=False)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_FILENAME = PROJECT_ROOT / "data" / "data_dump_accrual_accounts.xlsx"


@app.command()
def query(
        prompt: Annotated[
            str,
            typer.Option(
                ...,
                "--prompt",
                "-p",
                help="Natural-language question.",
            ),
        ],
        filename: Annotated[
            Path,
            typer.Option(
                "--filename",
                "-f",
                help="Path to Excel file.",
            ),
        ] = DEFAULT_DATA_FILENAME,
) -> None:
    request_model = AiExtractionPipelineQueryRequestModel(filename, prompt)
    console = Console()
    use_case = AiExtractionPipelineQueryUseCase(
        tabular_data_service=PandasExcelDataService(),
        llm_query_service=OpenAIPandasqlService(),
    )
    response_model = use_case.execute(request_model)

    if isinstance(response_model, UseCaseExceptionResponse):
        console.print(f"[red]Error:[/red] {response_model.message}")
        raise typer.Exit(code=response_model.exit_code)

    console.print(f"Summary: {response_model.summary}")
    console.print(f"SQL: {response_model.generated_sql}")
    console.print(f"Rows: {response_model.result_rows}")
    console.print("Result preview:")

    if not response_model.preview_rows:
        console.print("No rows returned.")
    else:
        table = Table(show_header=True, header_style="bold")
        for column in response_model.preview_columns:
            table.add_column(column, overflow="fold")
        for row in response_model.preview_rows:
            table.add_row(*row)
        console.print(table)

        if response_model.preview_truncated:
            shown_rows = len(response_model.preview_rows)
            console.print(
                f"[dim]Showing first {shown_rows} rows out of "
                f"{response_model.result_rows} total rows.[/dim]",
            )

    raise typer.Exit(code=response_model.exit_code)


if __name__ == "__main__":
    app()
