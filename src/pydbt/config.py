from dataclasses import dataclass
from typing import Literal, Optional, Dict, Any
from pathlib import Path
import os
from dotenv import dotenv_values

BackendType = Literal["duckdb", "postgres", "bigquery", "snowflake"]

VALID_BACKENDS = {"duckdb", "postgres", "bigquery", "snowflake"}

@dataclass
class ConnectionConfig:
    backend: BackendType
    connection_params: Dict[str, Any]

    @classmethod
    def from_env(cls, env_path: Path) -> "ConnectionConfig":
        config = dotenv_values(env_path)
        
        backend = config.get("PYDBT_BACKEND")
        if not backend:
            raise ValueError("PYDBT_BACKEND must be set in .env file")
            
        if backend not in VALID_BACKENDS:
            raise ValueError(
                f"Invalid backend: {backend}. Must be one of: {', '.join(VALID_BACKENDS)}"
            )            
        if backend == "duckdb":
            params = {"path": config.get("DUCKDB_PATH", ":memory:")}
        elif backend == "postgres":
            params = {
                "host": config.get("PG_HOST"),
                "port": config.get("PG_PORT"),
                "user": config.get("PG_USER"),
                "password": config.get("PG_PASSWORD"),
                "database": config.get("PG_DATABASE"),
            }
        elif backend == "bigquery":
            params = {
                "project_id": config.get("BQ_PROJECT"),
                "credentials_path": config.get("BQ_CREDENTIALS"),
            }
        else:  # snowflake
            params = {
                "account": config.get("SF_ACCOUNT"),
                "user": config.get("SF_USER"),
                "password": config.get("SF_PASSWORD"),
                "database": config.get("SF_DATABASE"),
                "warehouse": config.get("SF_WAREHOUSE"),
            }
            
        return cls(backend=backend, connection_params=params)

