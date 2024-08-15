import requests
from bs4 import BeautifulSoup
import csv

# URL do site que você deseja fazer scraping
url = 'https://abeoc.org.br/2014/06/agm-turismo/'  # Substitua com a URL real

output_csv = 'web.csv'

# Faz uma requisição HTTP para o site
page = requests.get(url)

# Analisa o conteúdo da página com BeautifulSoup
soup = BeautifulSoup(page.text, 'html.parser')

# Encontra o elemento <div> com a classe 'entry-content'
div_content = soup.find('div', class_='entry-content')

# Verifica se a <div> foi encontrada
if div_content:
    # Obtém o conteúdo HTML da <div>
    html_content = div_content.decode_contents()
    
    # Abre o arquivo CSV e inicializa o escritor
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Escrever o cabeçalho
        writer.writerow(['HTML da Div'])
        
        # Escreve o conteúdo HTML no CSV
        writer.writerow([html_content])
else:
    print("A div com a classe 'entry-content' não foi encontrada.")
