from abc import abstractmethod

from use_cases.request_models.ai_extraction_pipeline_query_request_model import RequestModel


class UseCase:

    @abstractmethod
    def execute(self, request_model: RequestModel):
        raise NotImplementedError
