from pathlib import Path

import pandas as pd

from tests.mocks import (
    FailingTabularDataService,
    MockLlmQueryService,
    MockTabularDataService,
)
from use_cases.ai_extraction_pipeline_query_use_case import (
    AiExtractionPipelineQueryUseCase,
)
from use_cases.decorators.error_handler import UseCaseExceptionResponse
from use_cases.request_models.ai_extraction_pipeline_query_request_model import (
    AiExtractionPipelineQueryRequestModel,
)
from use_cases.response_models.ai_extraction_pipeline_query_response_model import (
    AiExtractionPipelineQueryResponseModel,
)


def test_execute_returns_success_response() -> None:
    use_case = AiExtractionPipelineQueryUseCase(
        tabular_data_service=MockTabularDataService(),
        llm_query_service=MockLlmQueryService(),
    )
    request_model = AiExtractionPipelineQueryRequestModel(
        filename=Path("data/data_dump_accrual_accounts.xlsx"),
        prompt="How many customers are there?",
    )

    result = use_case.execute(request_model)

    assert isinstance(result, AiExtractionPipelineQueryResponseModel)
    assert result.exit_code == 0
    assert result.generated_sql == "SELECT COUNT(*) AS total_customers FROM records"
    assert result.result_rows == 1
    assert result.preview_columns == ["total_customers"]
    assert result.preview_rows == [["3"]]
    assert result.preview_truncated is False
    assert result.summary == "There are 3 customers."


def test_execute_returns_exception_response_on_error() -> None:
    use_case = AiExtractionPipelineQueryUseCase(
        tabular_data_service=FailingTabularDataService(),
        llm_query_service=MockLlmQueryService(),
    )
    request_model = AiExtractionPipelineQueryRequestModel(
        filename=Path("missing.xlsx"),
        prompt="How many customers are there?",
    )

    result = use_case.execute(request_model)

    assert isinstance(result, UseCaseExceptionResponse)
    assert result.exit_code == 1
    assert "Missing file" in result.message


def test_execute_preview_is_limited_to_10_rows_for_large_result() -> None:
    use_case = AiExtractionPipelineQueryUseCase(
        tabular_data_service=MockTabularDataService(
            query_result_dataframe=pd.DataFrame({"value": list(range(20))}),
        ),
        llm_query_service=MockLlmQueryService(),
    )
    request_model = AiExtractionPipelineQueryRequestModel(
        filename=Path("data/data_dump_accrual_accounts.xlsx"),
        prompt="Show me all values",
    )

    result = use_case.execute(request_model)

    assert isinstance(result, AiExtractionPipelineQueryResponseModel)
    assert result.result_rows == 20
    assert len(result.preview_rows) == 10
    assert result.preview_rows[0] == ["0"]
    assert result.preview_rows[-1] == ["9"]
    assert result.preview_truncated is True
