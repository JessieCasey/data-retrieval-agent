import re

import pandas as pd
from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL, TABLE_NAME
from services.abstract.llm_query_service import LlmQueryService
from services.openai_prompts import (
    SQL_SYSTEM_PROMPT,
    SUMMARY_SYSTEM_PROMPT,
    build_sql_user_prompt,
    build_summary_user_prompt,
)


class OpenAIPandasqlService(LlmQueryService):
    def __init__(self) -> None:
        self.api_key = OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set.")

        self.model = OPENAI_MODEL
        self.table_name = TABLE_NAME
        self.client = OpenAI(api_key=self.api_key)

    def generate_sql(self, prompt: str, dataframe: pd.DataFrame) -> str:
        schema = self._build_schema(dataframe)
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": SQL_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": build_sql_user_prompt(
                        table_name=self.table_name,
                        schema=schema,
                        prompt=prompt,
                    ),
                },
            ],
        )

        content = self._get_response_content(response)
        sql = self._extract_sql_from_structured_response(content)
        sql = self._enforce_select_only(sql)
        return sql

    def summarize_query_result(
        self,
        prompt: str,
        generated_sql: str,
        query_dataframe: pd.DataFrame,
    ) -> str:
        result_preview = self._build_result_preview(query_dataframe)
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": SUMMARY_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": build_summary_user_prompt(
                        prompt=prompt,
                        generated_sql=generated_sql,
                        row_count=len(query_dataframe.index),
                        result_preview=result_preview,
                    ),
                },
            ],
        )

        summary = self._get_response_content(response)
        if not summary:
            raise ValueError("LLM returned blank summary.")
        return summary

    def _build_schema(self, dataframe: pd.DataFrame) -> str:
        lines = ["Columns:"]
        for column in dataframe.columns:
            lines.append(
                f"- {self._quote_identifier(str(column))}: {dataframe[column].dtype}",
            )
        return "\n".join(lines)

    def _extract_sql_from_structured_response(self, content: str) -> str:
        match = re.search(
            r"BEGIN_SQL\s*(?P<sql>.*?)\s*END_SQL",
            content,
            flags=re.DOTALL,
        )
        if not match:
            raise ValueError(
                "LLM response does not follow required SQL structure: BEGIN_SQL ... END_SQL.",
            )

        sql = match.group("sql").strip()
        if not sql:
            raise ValueError("LLM returned empty SQL in structured response.")
        return sql

    def _enforce_select_only(self, sql: str) -> str:
        if not sql.lower().startswith("select"):
            raise ValueError("Generated SQL is not SELECT.")
        if ";" in sql:
            raise ValueError("Multiple SQL statements are not allowed.")
        return sql

    def _build_result_preview(self, query_dataframe: pd.DataFrame) -> str:
        if query_dataframe.empty:
            return "No rows returned."

        preview = query_dataframe.head(20)
        return preview.to_csv(index=False)

    def _get_response_content(self, response: object) -> str:
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("LLM returned empty content.")

        return content.strip()

    def _quote_identifier(self, identifier: str) -> str:
        escaped = identifier.replace('"', '""')
        return f'"{escaped}"'
