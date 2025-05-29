import pandas as pd

class DataFrameBuilder:
    @staticmethod
    def build_from_columns(df, columns):
        return pd.DataFrame(df[columns])
