import pandas as pd
from pydbt.testing import TestCase

# Define test cases
TEST_CASES = [
    TestCase(
        name="test_daily_registrations",
        description="Verify daily user registration counts",
        input_data={
            "users": pd.DataFrame({
                "id": [1, 2, 3, 4, 5],
                "registration_date": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-02",
                    "2024-01-03"
                ]
            })
        },
        expected_output=pd.DataFrame({
            "registration_date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "daily_registrations": [2, 2, 1]
        })
    )
]