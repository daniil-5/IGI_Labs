class WageSpeedAnalyzer:
    def __init__(self, df):
        # remove the empty strings
        self.df = df.dropna(subset=['Wage', 'Sprint speed'])

    def average_speed_below_average_wage(self):
        average_wage = self.df['Wage'].mean()
        filtered = self.df[self.df['Wage'] < average_wage]
        return round(filtered['Sprint speed'].mean(), 2)