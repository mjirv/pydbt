from dataclasses import dataclass
from typing import Literal, Optional, Dict, Any
from pathlib import Path
import os
from dotenv import load_dotenv

BackendType = Literal["duckdb", "postgres", "bigquery", "snowflake"]

@dataclass
class ConnectionConfig:
    backend: BackendType
    connection_params: Dict[str, Any]

    @classmethod
    def from_env(cls, env_path: Path) -> "ConnectionConfig":
        load_dotenv(env_path)
        
        backend = os.getenv("PYDBT_BACKEND")
        if backend not in ("duckdb", "postgres", "bigquery", "snowflake"):
            raise ValueError(f"Unsupported backend: {backend}")
            
        if backend == "duckdb":
            params = {"path": os.getenv("DUCKDB_PATH", ":memory:")}
        elif backend == "postgres":
            params = {
                "host": os.getenv("PG_HOST"),
                "port": os.getenv("PG_PORT"),
                "user": os.getenv("PG_USER"),
                "password": os.getenv("PG_PASSWORD"),
                "database": os.getenv("PG_DATABASE"),
            }
        elif backend == "bigquery":
            params = {
                "project_id": os.getenv("BQ_PROJECT"),
                "credentials_path": os.getenv("BQ_CREDENTIALS"),
            }
        else:  # snowflake
            params = {
                "account": os.getenv("SF_ACCOUNT"),
                "user": os.getenv("SF_USER"),
                "password": os.getenv("SF_PASSWORD"),
                "database": os.getenv("SF_DATABASE"),
                "warehouse": os.getenv("SF_WAREHOUSE"),
            }
            
        return cls(backend=backend, connection_params=params)

