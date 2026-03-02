from abc import abstractmethod

from use_cases.request_models.request_model import RequestModel


class UseCase:
    @abstractmethod
    def execute(self, request_model: RequestModel):
        raise NotImplementedError
