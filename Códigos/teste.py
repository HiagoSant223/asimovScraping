import pandas as pd
import requests

url = 'http://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL'

response = requests.get(url)

dados_api = response.json()

print(dados_api)

df = pd.DataFrame(dados_api)

print(df)