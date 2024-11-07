# PyDBT

PyDBT is a Python-based helper tool for dbt projects that enables you to write models in Python using Ibis and automatically generate corresponding SQL files. Write your transformations in Python, test them with proper test cases, and let PyDBT handle the SQL generation.

## Features

- Write dbt models in Python using Ibis
- Automatic SQL generation from Python models
- Built-in testing framework
- Support for multiple database backends:
  - DuckDB
  - PostgreSQL
  - BigQuery
  - Snowflake
- Type hints throughout the codebase

## Installation

```bash
pip install pydbt
```

## Quick Start

1. In your dbt project, initialize PyDBT:

```bash
pydbt init
```

2. Copy `.env.example` to `.env` and configure your database connection:

```bash
cp pydbt/.env.example pydbt/.env
```

3. Write your first model in `pydbt/your_first_model.py`:

```python
def run(con, ibis):
    """
    Example model that creates a simple transformation.
    """
    users = con.table('users')
    return users.group_by('registration_date').aggregate(
        daily_registrations=lambda t: t.id.count()
    ).order_by('registration_date')
```

4. Add tests in `pydbt/your_first_model_test.py`:

```python
import pandas as pd
from pydbt.testing import TestCase

TEST_CASES = [
    TestCase(
        name="test_daily_registrations",
        description="Verify daily user registration counts",
        input_data={
            "users": pd.DataFrame({
                "id": [1, 2, 3],
                "registration_date": ["2024-01-01", "2024-01-01", "2024-01-02"]
            })
        },
        expected_output=pd.DataFrame({
            "registration_date": ["2024-01-01", "2024-01-02"],
            "daily_registrations": [2, 1]
        })
    )
]
```

5. Run tests:

```bash
pydbt test
```

6. Generate SQL:

```bash
pydbt run
```

This will create corresponding SQL files in your dbt `models` directory.

## Project Structure

```
your-dbt-project/
├── models/              # dbt SQL models (generated)
└── pydbt/              # PyDBT Python models
    ├── .env            # Connection configuration
    ├── .gitignore
    ├── your_first_model.py
    └── your_first_model_test.py
```

## Configuration

PyDBT uses a `.env` file for database configuration. Example configurations:

### DuckDB

```env
PYDBT_BACKEND=duckdb
DUCKDB_PATH=:memory:
```

### PostgreSQL

```env
PYDBT_BACKEND=postgres
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=postgres
PG_DATABASE=database
```

### BigQuery

```env
PYDBT_BACKEND=bigquery
BQ_PROJECT=your-project-id
BQ_CREDENTIALS=/path/to/credentials.json
```

### Snowflake

```env
PYDBT_BACKEND=snowflake
SF_ACCOUNT=your-account
SF_USER=your-user
SF_PASSWORD=your-password
SF_DATABASE=your-database
SF_WAREHOUSE=your-warehouse
```

## CLI Commands

- `pydbt init`: Initialize PyDBT in your dbt project
- `pydbt run`: Generate SQL files from Python models
- `pydbt test`: Run tests for all models
- `pydbt test --model model_name`: Test a specific model

## Writing Models

Each model should be a Python file in the `pydbt` directory that exports a `run` function:

```python
def run(con, ibis):
    """
    Args:
        con: Ibis connection
        ibis: Ibis module

    Returns:
        ibis.Expr: An Ibis expression that will be compiled to SQL
    """
    return con.table('source_table').my_transformation()
```

## Writing Tests

Tests live alongside models with a `_test` suffix. Each test file should define a `TEST_CASES` list:

```python
TEST_CASES = [
    TestCase(
        name="test_name",
        description="Test description",
        input_data={
            "table_name": pd.DataFrame(...)
        },
        expected_output=pd.DataFrame(...)
    )
]
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
