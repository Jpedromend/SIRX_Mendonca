import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ==========================================
# 1. SETUP
# ==========================================
# File paths for JHU COVID-19 time series data
# downloaded from https://github.com/CSSEGISandData/COVID-19
FILE_CONFIRMED = 'data/time_series_covid19_confirmed_global.csv'
FILE_DEATHS    = 'data/time_series_covid19_deaths_global.csv'
FILE_RECOVERED = 'data/time_series_covid19_recovered_global.csv'

# ==========================================
# 2. FUNCTIONS
# ==========================================

def process_jhu_data(df_c, df_d, df_r, country_name):
    """
    Extracts data for a specified country from JHU dataframes,
    aggregates provinces, aligns dates, and calculates Active cases.

    Returns:
        pandas.DataFrame: Cleaned time series data.
    """
    
    def extract_timeseries(df, value_name):
        # Filter by country and aggregate provinces/states
        subset = df[df['Country/Region'] == country_name].copy()
        ts = subset.drop(columns=['Lat', 'Long', 'Province/State', 'Country/Region']).sum(axis=0)
        
        # Convert index to datetime objects
        ts.index = pd.to_datetime(ts.index)
        ts.name = value_name
        return ts

    # Extract the three series: Confirmed, Deaths, Recovered
    series_c = extract_timeseries(df_c, 'Confirmed')
    series_d = extract_timeseries(df_d, 'Deaths')
    series_r = extract_timeseries(df_r, 'Recovered')

    # Combine into a single DataFrame (auto-aligns by date)
    df_clean = pd.concat([series_c, series_d, series_r], axis=1)

    # Calculate Active Cases: Active = Confirmed - Deaths - Recovered
    df_clean['Active'] = df_clean['Confirmed'] - df_clean['Deaths'] - df_clean['Recovered']

    # Filter: Start from the first day with Confirmed > 0
    df_clean = df_clean[df_clean['Confirmed'] > 0].copy()

    # Add 'Day' column (integer index starting from 1)
    df_clean.index.name = 'Date'
    df_clean = df_clean.reset_index()
    df_clean['Day'] = df_clean.index + 1

    return df_clean

def plot_active_cases(df, country_name):
    """
    Plots the Active cases over time.
    """
    plt.figure(figsize=(10, 6))
    
    # Plot Data
    plt.plot(df['Date'], df['Active'], 's', color='black', fillstyle='none')
    
    # Formatting
    plt.title(f'Real Data Extraction: {country_name}', fontsize=16)
    plt.ylabel('Active Cases', fontsize=14)
    plt.xlabel('Date', fontsize=14)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    plt.ylim(bottom=0)
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    # Configure X-Axis Date Formatting
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1)) # Tick every week
    plt.gcf().autofmt_xdate() # Rotate dates for readability
    
    plt.tight_layout()
    plt.show()

# ==========================================
# 3. MAIN EXECUTION
# ==========================================

# Example input
COUNTRY = 'Spain'

print(f"--- Loading JHU Data for {COUNTRY} ---")

# Load Raw CSVs
raw_conf = pd.read_csv(FILE_CONFIRMED)
raw_dead = pd.read_csv(FILE_DEATHS)
raw_recov = pd.read_csv(FILE_RECOVERED)

# Process Data
print("Processing and cleaning data...")
clean_data = process_jhu_data(raw_conf, raw_dead, raw_recov, COUNTRY)

# Save to CSV
output_filename = f"data_{COUNTRY.lower()}.csv"
print(f"Saving processed data to: {output_filename}")
clean_data.to_csv(output_filename, index=False, float_format='%.0f')

# Display first few rows to verify
print("\nFirst 5 rows of processed data:")
print(clean_data.head())

# Plot
print("\nPlotting active cases...")
plot_active_cases(clean_data, COUNTRY)
