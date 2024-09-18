import requests
from bs4 import BeautifulSoup
import pandas as pd

def scraping_uf(uf: str):
    uf_url = f'https://www.ibge.gov.br/cidades-e-estados/{uf}.html'
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
    page = requests.get(uf_url, headers=headers)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    indicadores = soup.select('.indicador')
    
    uf_dict = {
        dado.select('.ind-label')[0].text.strip(): dado.select('.ind-value')[0].text.strip()
        for dado in indicadores
        if dado.select('.ind-label') and dado.select('.ind-value')
    }
    
    return uf_dict

estado = scraping_uf('rs')  # Chama a função e armazena o resultado em estado

# Função para limpar caracteres indesejados
def limpar_texto(texto):
    # Remove caracteres não imprimíveis e espaços em branco extras
    texto = texto.replace('\xa0', ' ').strip()  # Substitui \xa0 por espaço e remove espaços em branco
    if ']' in texto:
        texto = texto.split(']')[0].strip()  # Remove texto após ']'
    return texto

# Aplica a função de limpeza em todos os valores do dicionário
estado = {chave: limpar_texto(valor) for chave, valor in estado.items()}

df = pd.DataFrame(estado.values(), index=estado.keys())
df

print(df)




