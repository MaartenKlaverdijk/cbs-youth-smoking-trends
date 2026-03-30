"""
main.py - CBS youth smoking + e-cigarette trends (age 16-19)

Author: Maarten Klaverdijk
Date: 2026-03-30

Purpose: Analyze trends in cigarette and e-cigarette use among Dutch youth (age 16–19)
         using CBS open data (dataset 85457ENG). Produce one chart and export data
         for reproducible analysis.

Dataset: CBS Open Data Portal - Life style; personal characteristics (85457ENG)
         https://opendata.cbs.nl/#/CBS/nl/dataset/85457ENG/table

Dependencies:
- Python 3.x
- pandas, matpplotlib, requests
"""

# Import libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt


# Configure data source, columns of interest, age category code, and ecig data start year
BASE_URL = "https://opendata.cbs.nl/ODataApi/odata/85457ENG/"
DATA_URL = BASE_URL + "TypedDataSet"

SMOKING_COL = "Smokers_1"
ECIG_COL = "ECigarette12YearsOrOlder_14"

AGE_CODE = "53080"  # code for age group 16–19
ECIG_START_YEAR = 2019

# Define events for vertical lines (year: label)
EVENTS = {
    2019: ("E-cigarette data starts"),
    2024: ("Ban on sweet-\nflavored vapes")
}


# Data functions
def get_data():
    """Download CBS dataset and return as DataFrame."""
    response = requests.get(DATA_URL)
    return pd.json_normalize(response.json()['value'])

def prepare_data_with_ci(df, column):
    """Get mean and 95% CI for a column by year for age 16-19."""
    # Keep only rows for selectged age group and related margins
    df = df[(df['Characteristics'].str.strip() == AGE_CODE) & 
            (df['Margins'].isin(['MW00000', 'MOG0095', 'MBG0095']))].copy()

    # Make a 'Year' column (key example: 2014JJ00)
    df['Year'] = df['Periods'].str[:4].astype(int)

    # Pivot so we have columns: mean, low, high
    df = df.pivot(index='Year', columns='Margins', values=column).reset_index()
    df = df.rename(columns={'MW00000': 'mean', 'MOG0095': 'low', 'MBG0095': 'high'})

    return df


# Make the dataset
def build_dataset(df):
    """Combine smoking and e-cigarette datasets, and calculate total exposure."""

    # Get smoking and ecig data
    smoking = prepare_data_with_ci(df, SMOKING_COL)
    ecig = prepare_data_with_ci(df, ECIG_COL)

    # Merge data
    df_combined = pd.merge(
        smoking,
        ecig,
        on='Year',
        how='left',
        suffixes=('_smoking', '_ecig')
    )

    # Add new column with approximate total smoking product use
    df_combined['total'] = df_combined['mean_smoking'] + df_combined['mean_ecig'].fillna(0)

    return df_combined.sort_values('Year')


# Plot results
def plot(df, save_path=None):
    """Plot smoking trends with confidence intervals, total exposure, and events."""
    plt.figure(figsize=(10, 6))

    # Cigarette line with CI
    plt.plot(df['Year'], df['mean_smoking'], marker='o', linewidth=2, label='Smoking')
    plt.fill_between(df['Year'], df['low_smoking'], df['high_smoking'], alpha=0.2)

    # E-cigarette line with CI
    plt.plot(df['Year'], df['mean_ecig'], marker='o', linewidth=2, label='E-cigarettes')
    plt.fill_between(df['Year'], df['low_ecig'], df['high_ecig'], alpha=0.2)

    # Approximate total smoking product use line (starting from ECIG_START_YEAR)
    total_years = df['Year'] >= ECIG_START_YEAR
    plt.plot(df.loc[total_years, 'Year'], df.loc[total_years, 'total'],
             linestyle='--', linewidth=2, label='Total smoking product use (approx.)')

    # Add vertical event lines with labels
    ymax = max(df['mean_smoking'].max(), df['mean_ecig'].max(skipna=True))
    for year, label in EVENTS.items():
        plt.axvline(x=year, linestyle='--', color='grey', alpha=0.7)
        plt.text(year + 0.1, ymax + 3, label, fontsize=10, rotation=0, va='bottom')

    # Apply labels and plot styling
    plt.title("Cigarette smoking decline vs. rising e-cigarette use in Dutch youth (16–19)", fontsize=14)
    plt.xlabel("Year", fontsize=16, fontweight='bold')
    plt.ylabel("Prevalence (%)", fontsize=16, fontweight='bold')
    plt.xticks(df['Year'], fontsize=12)
    plt.grid(alpha=0.3)
    plt.legend(fontsize=12)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


# Main
if __name__ == "__main__":
    df_raw = get_data()
    df_final = build_dataset(df_raw)
    plot(df_final, save_path="youth_smoking_trends.png")
