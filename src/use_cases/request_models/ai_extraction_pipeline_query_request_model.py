from dataclasses import dataclass

from data_retrieval_agent.use_cases.request_models.request_model import RequestModel


@dataclass
class AiExtractionPipelineQueryRequestModel(RequestModel):
    filename: str
    prompt: str
