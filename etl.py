import os
import requests
import json
import psycopg2
import matplotlib.pyplot as plt

def load_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def extract_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def load_weather_data(db_config, weather_data):
    connection = None
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Create table if it doesn't exist
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS public.weather (
            id SERIAL PRIMARY KEY,
            city VARCHAR(50),
            temperature FLOAT,
            humidity INT,
            description VARCHAR(100),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_table_query)

        # Insert data into the table
        insert_query = '''
        INSERT INTO weather (city, temperature, humidity, description)
        VALUES (%s, %s, %s, %s);
        '''
        cursor.execute(insert_query, (
            weather_data['name'],
            weather_data['main']['temp'],
            weather_data['main']['humidity'],
            weather_data['weather'][0]['description']
        ))

        connection.commit()
        print("Data loaded successfully.")

    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def visualize_weather_data(db_config):
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Query the weather data
        cursor.execute("SELECT city, temperature, humidity FROM weather;")
        rows = cursor.fetchall()

        # Prepare data for visualization
        cities = [row[0] for row in rows]
        temperatures = [row[1] for row in rows]
        humidities = [row[2] for row in rows]

        # Create a bar plot for temperatures
        plt.figure(figsize=(10, 5))
        plt.bar(cities, temperatures, color='blue', alpha=0.7, label='Temperature (°C)')
        plt.ylabel('Temperature (°C)')
        plt.title('Weather Data: Temperature by City')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Save the plot as an image file
        plt.savefig("temperature_plot.png")
        plt.show()

    except Exception as e:
        print(f"Error visualizing data: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":

    config = load_config('config.json')
    api_key = config['api_key']
    db_config = config['db_config']
   
    cities = config['cities']

    for city in cities:
          weather_data = extract_weather_data(api_key, city)
          if weather_data:
              load_weather_data(db_config, weather_data)

visualize_weather_data(db_config)

