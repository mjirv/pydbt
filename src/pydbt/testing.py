from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
import pandas as pd
import ibis
from pathlib import Path
import importlib.util
from .config import ConnectionConfig

@dataclass
class TestCase:
    name: str
    input_data: Dict[str, pd.DataFrame]
    expected_output: pd.DataFrame
    description: Optional[str] = None

class ModelTester:
    def __init__(self, model_path: Path, test_path: Path):
        self.model_path = model_path
        self.test_path = test_path
        self.model = self._load_module(model_path)
        self.tests = self._load_module(test_path)

    @staticmethod
    def _load_module(path: Path) -> Any:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if not spec or not spec.loader:
            raise ImportError(f"Could not load {path}")
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run_tests(self) -> List[Dict[str, Any]]:
        """Run all test cases for the model."""
        results = []
        
        # Create in-memory DuckDB connection for testing
        con = ibis.duckdb.connect(":memory:")
        
        for test_case in self.tests.TEST_CASES:
            # Load test data into tables
            tables = {}
            for table_name, df in test_case.input_data.items():
                tables[table_name] = con.create_table(table_name, df)
            
            # Run the model
            try:
                result = self.model.run(con, ibis)
                actual_df = result.execute()
                
                # Compare with expected output
                pd.testing.assert_frame_equal(
                    actual_df.reset_index(drop=True),
                    test_case.expected_output.reset_index(drop=True)
                )
                
                results.append({
                    "name": test_case.name,
                    "success": True,
                    "message": test_case.description or "Test passed"
                })
            except Exception as e:
                results.append({
                    "name": test_case.name,
                    "success": False,
                    "message": str(e)
                })
            
            # Clean up tables
            for table in tables.values():
                table.drop()
        
        return results
