SQL_SYSTEM_PROMPT = """
You generate one SQLite SELECT query for pandasql.
STRICT OUTPUT FORMAT:
BEGIN_SQL
<single SELECT query>
END_SQL
RULES:
- Return exactly one SELECT statement.
- Do not use markdown or code fences.
- Do not add explanation text.
- Do not include more than one SQL statement.
- If a column contains spaces or symbols, wrap it in double quotes.
EXAMPLES:
BEGIN_SQL
SELECT COUNT(*) AS total_rows FROM records
END_SQL
BEGIN_SQL
SELECT customer_id, amount FROM records WHERE amount > 1000
END_SQL
BEGIN_SQL
SELECT COUNT(DISTINCT "Unnamed: 0") AS total_customers FROM records
END_SQL
""".strip()

SUMMARY_SYSTEM_PROMPT = """
You are a data analyst. Provide a short summary in 1-2 sentences.
Be clear and concise for non-technical users.
""".strip()


def build_sql_user_prompt(*, table_name: str, schema: str, prompt: str) -> str:
    return f"""
        Table: {table_name}
        {schema}
        Question: {prompt}
        Use column names exactly as listed in schema. Keep quotes for names with special characters.
        Return output only in this format:
        BEGIN_SQL
        <single SELECT query>
        END_SQL
    z""".strip()


def build_summary_user_prompt(
    *,
    prompt: str,
    generated_sql: str,
    row_count: int,
    result_preview: str,
) -> str:
    return f"""
        Question: {prompt}
        SQL used: {generated_sql}
        Row count: {row_count}
        Result preview:
        {result_preview}
    """.strip()
