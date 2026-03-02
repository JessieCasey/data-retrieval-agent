import pandas as pd

from services.abstract.llm_query_service import LlmQueryService
from services.abstract.tabular_data_service import TabularDataService
from use_cases.abstract.use_case import UseCase
from use_cases.decorators.error_handler import ExceptionHandler, UseCaseExceptionResponse
from use_cases.request_models.ai_extraction_pipeline_query_request_model import \
    AiExtractionPipelineQueryRequestModel
from use_cases.response_models.ai_extraction_pipeline_query_response_model import \
    AiExtractionPipelineQueryResponseModel


class AiExtractionPipelineQueryUseCase(UseCase):
    def __init__(
        self,
        tabular_data_service: TabularDataService,
        llm_query_service: LlmQueryService,
    ) -> None:
        self.tabular_data_service = tabular_data_service
        self.llm_query_service = llm_query_service

    @ExceptionHandler
    def execute(
        self,
        request_model: AiExtractionPipelineQueryRequestModel,
    ) -> AiExtractionPipelineQueryResponseModel | UseCaseExceptionResponse:
        dataframe: pd.DataFrame = self.tabular_data_service.load_excel(request_model.filename)
        generated_sql = self.llm_query_service.generate_sql(request_model.prompt, dataframe)
        query_dataframe = self.tabular_data_service.execute_sql(generated_sql, dataframe)
        summary = self.llm_query_service.summarize_query_result(
            request_model.prompt,
            generated_sql,
            query_dataframe,
        )

        return AiExtractionPipelineQueryResponseModel(
            exit_code=0,
            filename=str(request_model.filename),
            prompt=request_model.prompt,
            generated_sql=generated_sql,
            result_rows=len(query_dataframe.index),
            summary=summary,
        )
