import requests 
from tinydb import TinyDB
from datetime import datetime
import time

def extract_bitcoin_data():
    url = "https://api.coinbase.com/v2/prices/spot"
    
    response = requests.get(url)
    data = response.json()
    return data

def transform_bitcoin_data(data):
    valor = data['data']['amount']
    criptomoeda = data['data']['base']
    moeda = data['data']['currency']
    timestamp = datetime.now().timestamp()

    transformed_data = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }
    return transformed_data

def load_bitcoin_tinydb(data, db_name='bitcoin_json'):
    db = TinyDB(db_name)
    db.insert(data)
    print("Carregamento realizado com sucesso")

if __name__=='__main__':
    while True:
        data = extract_bitcoin_data()
        transformed_data = transform_bitcoin_data(data)
        load_bitcoin_tinydb(transformed_data)
        time.sleep(12)