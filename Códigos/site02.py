# import requests
# from bs4 import BeautifulSoup

# # URL do site
# url = 'https://abrape.com.br/associados/?jsf=jet-engine:lista&tax=estado:263'

# # Requisição HTTP
# response = requests.get(url)

# # Criação do objeto BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')

# # Encontrar todas as <div> com a classe 'elementor-widget-wrap elementor-element-populated'
# divs = soup.find_all('div', class_='elementor elementor-327')

# # Iterar sobre as divs encontradas
# for div in divs:
#     # Encontrar todos os elementos <p> dentro da div
#     paragraphs = div.find_all('p')
    
#     # Printar o texto de cada <p>
#     for p in paragraphs:
#         print(p.get_text())

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

# Configuração do Firefox em modo headless
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

try:
    # URL que você deseja acessar
    url = 'https://abrape.com.br/associados/?jsf=jet-engine:lista&tax=estado:263'
    driver.get(url)
    print(f'Acessando: {url}')
    
    # Aguarde o carregamento completo da página
    time.sleep(5)  # Ajuste o tempo conforme necessário

    # Encontrar todos os elementos com as classes especificadas
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.elementor.elementor-327')
    
    for element in elements:
        try:
            print(f'Clicando no elemento: {element.text}')
            element.click()
            
            # Aguarde um pouco após o clique para garantir que a ação seja completada
            time.sleep(15)  # Ajuste o tempo conforme necessário
            
            # Voltar para a página anterior
            driver.back()
            
            # Aguarde o carregamento da página após voltar
            time.sleep(5)  # Ajuste o tempo conforme necessário
            
            # Re-encontrar os elementos após voltar à página anterior
            elements = driver.find_elements(By.CSS_SELECTOR, 'div.elementor.elementor-327')
        
        except Exception as e:
            print(f'Erro ao clicar no elemento: {e}')

finally:
    driver.quit()
    print("Navegação concluída.")
    
# Código atual realiza acesso a URL > identifica todos os elementos > tenta realizar um clique..
