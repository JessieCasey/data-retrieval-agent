from pathlib import Path

import typer

from use_cases.ai_extraction_pipeline_query_use_case import AiExtractionPipelineQueryUseCase
from use_cases.request_models.ai_extraction_pipeline_query_request_model import \
    AiExtractionPipelineQueryRequestModel

app = typer.Typer(help="data-retrieval-agent CLI")


@app.command()
def query(
        filename: Path = typer.Argument(..., help="Path to Excel file."),
        prompt: str = typer.Argument(..., help="Natural-language question."),
) -> None:
    request_model = AiExtractionPipelineQueryRequestModel(filename, prompt)
    use_case = AiExtractionPipelineQueryUseCase()
    response_model = use_case.execute(request_model)
    raise typer.Exit(code=response_model.exit_code)


if __name__ == "__main__":
    app()
