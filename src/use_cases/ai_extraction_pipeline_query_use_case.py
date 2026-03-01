from data_retrieval_agent.use_cases.abstract.use_case import UseCase
from data_retrieval_agent.use_cases.request_models.ai_extraction_pipeline_query_request_model import \
    AiExtractionPipelineQueryRequestModel
from data_retrieval_agent.use_cases.response_models.ai_extraction_pipeline_query_response_model import \
    AiExtractionPipelineQueryResponseModel


class AiExtractionPipelineQueryUseCase(UseCase):

    def execute(self, request_model: AiExtractionPipelineQueryRequestModel) -> AiExtractionPipelineQueryResponseModel:
        return 1
