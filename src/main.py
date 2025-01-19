import warnings
import os
from config import load_config
from weather_api import extract_weather_data
from database import load_weather_data, fetch_weather_data, fetch_rainy_cities
from visualization import visualize_weather_data, visualize_rainy_cities

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)

if __name__ == "__main__":
    config_path = os.path.join('config', 'config.json')
    config = load_config(config_path)
    
    api_key = config['api_key']
    db_config = config['db_config']
    cities = config['cities']

    # Extract and load weather data for each city
    for city in cities:
        weather_data = extract_weather_data(api_key, city)
        if weather_data:
            load_weather_data(db_config, weather_data)

    # Fetch and visualize weather data
    weather_data = fetch_weather_data(db_config)
    visualize_weather_data(weather_data)

    # Fetch and visualize rainy cities
    rainy_cities_data = fetch_rainy_cities(db_config)
    visualize_rainy_cities(rainy_cities_data)
