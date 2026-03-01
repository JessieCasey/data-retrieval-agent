from dataclasses import dataclass

from data_retrieval_agent.use_cases.response_models.response_model import ResponseModel


@dataclass
class AiExtractionPipelineQueryResponseModel(ResponseModel):
    exit_code: int
    filename: str
    prompt: str
