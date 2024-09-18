import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

# Lista de estados
estados = [
    'alagoas'
]

# Função para rolar a página até o final
def scroll_until_all_items_loaded(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Rolagem para o fim da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Aguarde o carregamento dos novos itens
        
        # Verificar a nova altura da página
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            # Se a altura não mudar, significa que todos os itens foram carregados
            break
        
        last_height = new_height

# Função para scraping de cada estado
def scraping_uf(uf: str):
    uf_url = f'https://abeoc.org.br/categoria/associados/{uf}/'
    option = Options()
    option.headless = True
    driver = webdriver.Firefox(options=option)
    driver.get(uf_url)
    
    try:
        # Rolar a página até o final para carregar todos os itens
        
        # Encontrar e clicar no primeiro 'div' com a classe 'post-meta'
        post_meta = driver.find_element(By.CSS_SELECTOR, 'div', class_="btn btn-xs btn-default text-xs text-uppercase")
        post_meta.click()
        
        # Esperar um pouco para a nova página carregar
        time.sleep(5)
        
        # Capturar o HTML da nova página
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Capturar todas as tags <p>
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        
        # Fechar o navegador
        driver.quit()
        
        return paragraphs
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f'Erro ao processar {uf}: {e}')
        driver.quit()
        return []

# Iterar sobre todos os estados e coletar dados
dados = []
for estado in estados:
    print(f'Coletando dados para {estado}...')
    paragraphs = scraping_uf(estado)
    for paragraph in paragraphs:
        dados.append({'estado': estado, 'texto': paragraph})

# Converter os dados para um DataFrame e salvar em CSV
df = pd.DataFrame(dados)
df.to_csv('dados_associados.csv', index=False)
print('Dados salvos em dados_associados.csv')
