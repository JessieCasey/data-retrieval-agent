from pathlib import Path

import typer

from services.openai_pandasql_service import OpenAIPandasqlService
from services.pandas_excel_data_service import PandasExcelDataService
from use_cases.ai_extraction_pipeline_query_use_case import AiExtractionPipelineQueryUseCase
from use_cases.decorators.error_handler import UseCaseExceptionResponse
from use_cases.request_models.ai_extraction_pipeline_query_request_model import \
    AiExtractionPipelineQueryRequestModel

app = typer.Typer(help="data-retrieval-agent CLI")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_FILENAME = PROJECT_ROOT / "data" / "data_dump_accrual_accounts.xlsx"


@app.command()
def query(
        prompt: str = typer.Option(
            ...,
            "--prompt",
            "-p",
            help="Natural-language question.",
        ),
        filename: Path = typer.Option(
            DEFAULT_DATA_FILENAME,
            "--filename",
            "-f",
            help="Path to Excel file.",
        ),
) -> None:
    request_model = AiExtractionPipelineQueryRequestModel(filename, prompt)
    use_case = AiExtractionPipelineQueryUseCase(
        tabular_data_service=PandasExcelDataService(),
        llm_query_service=OpenAIPandasqlService(),
    )
    response_model = use_case.execute(request_model)
    if isinstance(response_model, UseCaseExceptionResponse):
        typer.echo(f"Error: {response_model.message}")
        raise typer.Exit(code=response_model.exit_code)
    typer.echo(f"Summary: {response_model.summary}")
    typer.echo(f"SQL: {response_model.generated_sql}")
    typer.echo(f"Rows: {response_model.result_rows}")
    raise typer.Exit(code=response_model.exit_code)


if __name__ == "__main__":
    app()
