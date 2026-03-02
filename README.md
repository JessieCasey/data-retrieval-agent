# data-retrieval-agent

## Setup (macOS/Linux)

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Poetry in the active virtual environment:

```bash
pip install --upgrade pip
pip install poetry
```

Install project dependencies:

```bash
python -m poetry install
```

```bash
cp .env.example .env
```
Add your `OPENAI_API_KEY` to `.env`.

## Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install poetry
python -m poetry install
Copy-Item .env.example .env
```

## Run

Run with the default dataset:

```bash
python src/main.py --prompt "how many customers there?"
```

Run with a custom Excel file:

```bash
python src/main.py --prompt "how many customers there?" --filename "/absolute/path/to/file.xlsx"
```

Show CLI help:

```bash
python src/main.py --help
```

## Quality

```bash
python -m poetry run ruff check .
python -m poetry run ruff format .
python -m poetry run pytest
```
