import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the path for the visualizations folder
VISUALIZATIONS_DIR = os.path.join('visualizations')

# Create the visualizations directory if it doesn't exist
os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)

def visualize_weather_data(data):
    # Prepare data for visualization
    df = pd.DataFrame(data, columns=['City', 'Temperature (°C)', 'Humidity (%)', 'Rain (mm)'])

    # Create a bar plot for temperatures using Seaborn
    plt.figure(figsize=(12, 6))
    bar_plot = sns.barplot(x='City', y='Temperature (°C)', data=df, palette='coolwarm', alpha=0.9)

    # Add data labels on top of the bars
    for p in bar_plot.patches:
        bar_plot.annotate(f'{p.get_height():.1f}', 
                          (p.get_x() + p.get_width() / 2., p.get_height()), 
                          ha='center', va='bottom', 
                          fontsize=10, color='black', 
                          xytext=(0, 5), 
                          textcoords='offset points')

    # Customize the plot
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.title('Weather Data: Temperature by City', fontsize=14)
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save the plot as an image file in the visualizations folder
    plt.savefig(os.path.join(VISUALIZATIONS_DIR, "temperature_plot.png"))
    plt.show()

def visualize_rainy_cities(data):
    # Prepare data for visualization
    if data:
        df = pd.DataFrame(data, columns=['City', 'Rain (mm)'])

        # Create a bar plot for rainy cities using Seaborn
        plt.figure(figsize=(12, 6))
        bar_plot = sns.barplot(x='City', y='Rain (mm)', data=df, palette='Blues', alpha=0.9)

        # Add data labels on top of the bars
        for p in bar_plot.patches:
            bar_plot.annotate(f'{p.get_height():.1f}', 
                              (p.get_x() + p.get_width() / 2., p.get_height()), 
                              ha='center', va='bottom', 
                              fontsize=10, color='black', 
                              xytext=(0, 5), 
                              textcoords='offset points')

        # Customize the plot
        plt.ylabel('Rain (mm)', fontsize=12)
        plt.title('Cities Currently Experiencing Rain', fontsize=14)
        plt.xticks(rotation=90, fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save the plot as an image file in the visualizations folder
        plt.savefig(os.path.join(VISUALIZATIONS_DIR, "rainy_cities_plot.png"))
        plt.show()
    else:
        print("No cities currently experiencing rain.")
