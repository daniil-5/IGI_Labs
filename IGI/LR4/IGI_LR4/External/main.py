import pandas as pd

from External.data_loader import DataLoader
from External.series_analyzer import SeriesAnalyzer
from External.dataframe_builder import DataFrameBuilder
from External.wage_speed_analyzer import WageSpeedAnalyzer
from External.aggression_shotpower_analyzer import AggressionShotPowerAnalyzer
from IPython.display import display
import re

def correct_parse(value):
    if pd.isna(value):
        return None
    value = str(value).strip()
    match = re.fullmatch(r"(\d+)([+-]\d+)?", value)
    if not match:
        return None
    base = int(match.group(1))
    modifier = int(match.group(2)) if match.group(2) else 0
    return base + modifier

def dataset_analizer():
    # Load dataset
    loader = DataLoader('External/CompleteDataset.csv')
    df = loader.load_data()
    print(type(df))
    df['Wage'] = (
            df['Wage']
            .str.replace('€', '', regex=False)
            .str.replace('K', '', regex=False)
            .astype(float) * 1000
    )
    df['Sprint speed'] = df['Sprint speed'].apply(correct_parse)
    df['Shot power'] = df['Shot power'].apply(correct_parse)

    # Series analysis on ShotPower
    shot_power_series = df['Shot power']
    analyzer = SeriesAnalyzer(shot_power_series)
    print("Series Head:")
    display(analyzer.show_head())
    # using of iloc -- index in row and loc is index and column name in row
    print("Element at index 0:", analyzer.get_element_by_iloc(0))
    print("Element using .loc:", analyzer.get_element_by_loc(df, 0, 'Shot power'))

    # Build smaller DataFrame
    builder = DataFrameBuilder()
    df_small = builder.build_from_columns(df, ['Aggression', 'Shot power', 'Sprint speed', 'Wage'])
    print("\nSelected Columns DataFrame:")
    display(df_small.head(10))

    # Analyze wage and sprint speed
    wage_analyzer = WageSpeedAnalyzer(df)
    avg_speed = wage_analyzer.average_speed_below_average_wage()
    print(f"\nAverage SprintSpeed of players with wage below average: {avg_speed}")

    # Analyze aggression and shot power
    aggr_analyzer = AggressionShotPowerAnalyzer(df)
    ratio = aggr_analyzer.shot_power_ratio()
    print(f"ShotPower ratio (max vs min aggression): {ratio}")

if __name__ == '__main__':
    dataset_analizer()