import requests
from bs4 import BeautifulSoup

# URL do site que você deseja fazer scraping
url = 'https://abeoc.org.br/2018/07/doity-plataforma-de-eventos-2/'  # Substitua com a URL real

# Faz uma requisição HTTP para o site
page = requests.get(url)

# Analisa o conteúdo da página com BeautifulSoup
soup = BeautifulSoup(page.text, 'html.parser')

# Encontra o elemento <div> com a classe 'entry-content'
div_content = soup.find('div', class_='entry-content')

# Verifica se a <div> foi encontrada
if div_content:
    # Encontra todos os elementos <p> dentro da <div> com a classe 'entry-content'
    paragrafos = div_content.find_all('p')
    
    # Itera sobre cada elemento <p> e imprime o texto
    for p in range(len(paragrafos)):
        print(paragrafos[p].text)
