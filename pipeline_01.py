import requests
import psycopg2
from datetime import datetime
import time
from dotenv import load_dotenv
import os

# Carregar as configurações do arquivo .env
load_dotenv()

# Função para extrair dados do Bitcoin
def extract_bitcoin_data():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    data = response.json()
    return data

# Função para transformar os dados
def transform_bitcoin_data(data):
    return {
        "valor": float(data['data']['amount']),  # Convertendo o valor para float
        "criptomoeda": data['data']['base'],
        "moeda": data['data']['currency'],
        "timestamp": datetime.now()
    }

# Função para carregar os dados no PostgreSQL
def load_bitcoin_postgres(data):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO bitcoin_data (valor, criptomoeda, moeda, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (data['valor'], data['criptomoeda'], data['moeda'], data['timestamp']))
            conn.commit()
            print("Carregamento realizado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
    finally:
        if conn:
            conn.close()

# Criar tabela no banco de dados (executado apenas uma vez)
def create_table():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS bitcoin_data (
                    id SERIAL PRIMARY KEY,
                    valor NUMERIC NOT NULL,
                    criptomoeda VARCHAR(10) NOT NULL,
                    moeda VARCHAR(10) NOT NULL,
                    timestamp TIMESTAMP NOT NULL
                )
            """)
            conn.commit()
            print("Tabela criada/verificada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Criar tabela na inicialização
    create_table()

    # Loop principal
    try:
        while True:
            data = extract_bitcoin_data()
            transformed_data = transform_bitcoin_data(data)
            load_bitcoin_postgres(transformed_data)
            time.sleep(12)
    except KeyboardInterrupt:
        print("Execução interrompida pelo usuário.")
