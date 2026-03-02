from dataclasses import dataclass

from use_cases.response_models.response_model import ResponseModel


@dataclass
class AiExtractionPipelineQueryResponseModel(ResponseModel):
    exit_code: int
    filename: str
    prompt: str
    generated_sql: str
    result_rows: int
    preview_columns: list[str]
    preview_rows: list[list[str]]
    preview_truncated: bool
    summary: str
