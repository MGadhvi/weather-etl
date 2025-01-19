import psycopg2

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
            rain FLOAT DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_table_query)

        # Extract rain data (if available)
        rain_amount = weather_data.get('rain', {}).get('1h', 0)

        # Insert data into the table
        insert_query = '''
        INSERT INTO weather (city, temperature, humidity, description, rain)
        VALUES (%s, %s, %s, %s, %s);
        '''
        cursor.execute(insert_query, (
            weather_data['name'],
            weather_data['main']['temp'],
            weather_data['main']['humidity'],
            weather_data['weather'][0]['description'],
            rain_amount
        ))

        connection.commit()
        print("Data loaded successfully.")

    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def fetch_weather_data(db_config):
    connection = None
    data = []
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Query the weather data
        cursor.execute("SELECT city, temperature, humidity, rain FROM weather;")
        data = cursor.fetchall()

    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    return data

def fetch_rainy_cities(db_config):
    connection = None
    data = []
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Query the weather data for cities with rain
        cursor.execute("SELECT city, rain FROM weather WHERE rain > 0;")
        data = cursor.fetchall()

    except Exception as e:
        print(f"Error fetching rainy cities: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    return data
