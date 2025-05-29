class SeriesAnalyzer:
    def __init__(self, series):
        self.series = series

    def show_head(self, n=10):
        return self.series.head(n)

    def get_element_by_iloc(self, index):
        return self.series.iloc[index]

    def get_element_by_loc(self, df, row_index, column_name):
        return df.loc[row_index, column_name]