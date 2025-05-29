class AggressionShotPowerAnalyzer:
    def __init__(self, df):
        self.df = df.dropna(subset=['Aggression', 'Shot power'])

    def shot_power_ratio(self):
        max_aggr = self.df['Aggression'].max()
        min_aggr = self.df['Aggression'].min()

        max_group = self.df[self.df['Aggression'] == max_aggr]
        min_group = self.df[self.df['Aggression'] == min_aggr]

        max_mean = max_group['Shot power'].mean()
        min_mean = min_group['Shot power'].mean()

        return round(max_mean / min_mean, 2)