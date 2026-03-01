# data-retrieval-agent

Production-style PoC for a CLI "AI data analyst" that:

- Loads an Excel file into pandas
- Exposes the DataFrame as one SQL table with `pandasql`
- Uses OpenAI (`gpt-4o-mini`) to generate SQL from natural language questions
- Applies SQL guardrails (`SELECT`-only + enforced `LIMIT`)
- Executes SQL and prints readable results in the terminal

## Requirements

- Python 3.11+
- OpenAI API key

## Setup

Linux/macOS (zsh/bash):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install poetry
python -m poetry install
cp .env.example .env
```

Windows (PowerShell):

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
pip install poetry
py -m poetry install
Copy-Item .env.example .env
```

Set `OPENAI_API_KEY` in `.env`.

## Run

```bash
python src/data_retrieval_agent/main.py "data/Data Dump - Accrual Accounts.xlsx" "Show top 10 rows"
```

## Development

```bash
python -m poetry run ruff check .
python -m poetry run ruff format .
python -m poetry run mypy .
python -m poetry run pytest
```

## Project layout

```text
data-retrieval-agent/
  pyproject.toml
  README.md
  .env.example
  .gitignore
  data/
    Data Dump - Accrual Accounts.xlsx
  src/
    data_retrieval_agent/
      __init__.py
      main.py
      cli.py
      use_case.py
      ports.py
      config.py
      datastore.py
      llm.py
      prompts.py
      sql_executor.py
      answer.py
      app_types.py
  tests/
    test_sql_executor.py
```
