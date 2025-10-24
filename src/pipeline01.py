import requests
import psycopg2
from datetime import datetime
import time
from dotenv import load_dotenv
import os

# Load the settings from the .env file
load_dotenv()


# Function to extract data from Bitcoin
def extract_bitcoin_data():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    data = response.json()
    return data


# Function to transform the data
def transform_bitcoin_data(data):
    return {
        "value": float(data["data"]["amount"]),  # Converting the value to float
        "cryptocurrency": data["data"]["base"],
        "currency": data["data"]["currency"],
        "timestamp": datetime.now(),
    }


# Function to load the data into PostgreSQL
def load_bitcoin_postgres(data):
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO bitcoin_data (value, cryptocurrency, currency, timestamp)
                VALUES (%s, %s, %s, %s)
            """,
                (
                    data["value"],
                    data["cryptocurrency"],
                    data["currency"],
                    data["timestamp"],
                ),
            )
            conn.commit()
            print("Loading completed successfully!")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        if conn:
            conn.close()


# Create table in the database (executed only once)
def create_table():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS bitcoin_data (
                    id SERIAL PRIMARY KEY,
                    value NUMERIC NOT NULL,
                    cryptocurrency VARCHAR(10) NOT NULL,
                    currency VARCHAR(10) NOT NULL,
                    timestamp TIMESTAMP NOT NULL
                )
            """
            )
            conn.commit()
            print("Table created/veridied successfully")
    except Exception as e:
        print(f"Erro crating table: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":

    # Creat table on initialization
    create_table()

    # Manin loop
    try:
        while True:
            data = extract_bitcoin_data()
            transformed_data = transform_bitcoin_data(data)
            load_bitcoin_postgres(transformed_data)
            time.sleep(12)
    except KeyboardInterrupt:
        print("Execution interrupted by the user")
