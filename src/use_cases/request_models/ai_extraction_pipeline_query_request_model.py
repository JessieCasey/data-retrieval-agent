from dataclasses import dataclass
from pathlib import Path

from use_cases.request_models.request_model import RequestModel


@dataclass
class AiExtractionPipelineQueryRequestModel(RequestModel):
    filename: Path
    prompt: str
