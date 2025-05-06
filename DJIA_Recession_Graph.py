import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import ipywidgets as widgets
from IPython.display import display


# Load the CSVs
sahm_df = pd.read_csv("SAHMREALTIME.csv")
djia_df = pd.read_csv("DJIA.csv")



# Format dates
sahm_df['Date'] = pd.to_datetime(sahm_df['observation_date'])
djia_df['Date'] = pd.to_datetime(djia_df['observation_date'])


# Clean up
sahm_df = sahm_df[['Date', 'SAHMREALTIME']]
djia_df = djia_df[['Date', 'DJIA']]

# Merge
merged_df = pd.merge(djia_df, sahm_df, on='Date', how='inner')
merged_df['DJIA'] = merged_df['DJIA'].ffill().bfill()


# Create recession indicator
merged_df['Recession'] = (merged_df['SAHMREALTIME'] >= 0.5).astype(int)

# Define the update function
def update_plot(start_year):
    fig, ax1 = plt.subplots(figsize=(14, 10))  # Create a figure and main axis

    # Plot DJIA on the primary y-axis (left)
    ax1.plot(merged_df['Date'], merged_df['DJIA'], label='DJIA', color='green')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Dow Jones Index", color='green')
    ax1.tick_params(axis='y', labelcolor='green')

    # Create a secondary y-axis for recession percentage points
    ax2 = ax1.twinx()
    ax2.plot(merged_df['Date'], merged_df['SAHMREALTIME'], label='Recession Indicator', color='red', linestyle='--')
    ax2.set_ylabel("Sahm Rule Percentage Points", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Dynamically adjust x-axis based on slider input
    ax1.set_xlim(pd.Timestamp(f"{start_year}-01-01"), pd.Timestamp(f"{start_year + 2}-01-01"))  # Show a 2-year window
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax1.tick_params(axis='x', rotation=45)

    # Title & Legend
    plt.title("Dow Jones Industrial Average vs. Sahm Rule Recession Indicator")
    fig.tight_layout()
    plt.legend()
    plt.show()



# Create a slider and link it properly
slider = widgets.IntSlider(min=2015, max=2025, step=1, value=2016, description="Scroll Year")

# Use `interactive` to connect the slider with the function properly
interactive_plot = widgets.interactive(update_plot, start_year=slider)

# Display both the plot and the slider together
display(interactive_plot)

# Plot
sns.set(style="whitegrid")
plt.figure(figsize=(42, 6))
plt.plot(merged_df['Date'], merged_df['DJIA'], label='DJIA', color='green')


plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks to monthly
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Show as "Jan 2024", "Feb 2024"...
# Shade recession periods
plt.fill_between(merged_df['Date'], merged_df['DJIA'].min(), merged_df['DJIA'].max(),
                 where=merged_df['Recession'] == 1, color='red', alpha=0.3, label='Recession (Sahm Rule)')

plt.title("Dow Jones Industrial Average vs. Sahm Rule Recession Indicator")
plt.xlabel("Date")
plt.ylabel("Dow Jones Index")
plt.legend()
plt.xticks(rotation=45)  # Rotate labels for better readability
plt.tight_layout()
plt.show()
