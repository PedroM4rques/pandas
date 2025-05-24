import pandas as pd
from unittest.mock import patch
from pandas.core.accessor import DataFrameAccessorLoader

def test_load_dataframe_accessors():
    # GH29076
    # Mocked EntryPoint to simulate a plugin
    class MockEntryPoint:
        name = "test_accessor"
        def load(self):
            class TestAccessor:
                def __init__(self, df):
                    self._df = df
                def test_method(self):
                    return "success"
            return TestAccessor

    # Patch the entry_points function to return the mocked plugin
    with patch("pandas.core.accessor.entry_points", return_value=[MockEntryPoint()]):
        DataFrameAccessorLoader.load()

        # Create DataFrame and verify that the accessor was registered
        df = pd.DataFrame({"a": [1, 2, 3]})
        assert hasattr(df, "test_accessor")
        assert df.test_accessor.test_method() == "success"
