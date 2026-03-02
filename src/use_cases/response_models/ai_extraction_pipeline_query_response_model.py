from dataclasses import dataclass

from use_cases.response_models.response_model import ResponseModel


@dataclass
class AiExtractionPipelineQueryResponseModel(ResponseModel):
    exit_code: int
    filename: str
    prompt: str
    generated_sql: str
    result_rows: int
    summary: str
