from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import csv

# Lista de estados
estados = [
    'sao-paulo'  # Adicione mais estados conforme necessário
]

# Configuração do Firefox em modo headless
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

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

def process_page(url, writer):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Garante que a requisição foi bem-sucedida
        
        # Tentar detectar o encoding correto automaticamente
        soup = BeautifulSoup(response.content, 'html.parser')
        detected_encoding = soup.original_encoding
        
        # Se o encoding detectado não for UTF-8, configurá-lo manualmente
        if detected_encoding.lower() != 'utf-8':
            response.encoding = detected_encoding

        content_div = soup.select_one('div.entry-content')

        if content_div:
            paragraphs = content_div.select('p')
            for p in paragraphs:
                writer.writerow([p.text.strip()])
        else:
            print(f'Conteúdo não encontrado para a URL: {url}')
    except requests.RequestException as e:
        print(f'Erro ao requisitar a URL: {e}')


def save_to_csv(file_name, links):
    try:
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Texto'])  # Cabeçalho do CSV
            for link in links:
                process_page(link, writer)
    except IOError as e:
        print(f'Erro ao escrever no arquivo CSV: {e}')

try:
    all_links = set()
    
    for estado in estados:
        url = f'https://abeoc.org.br/categoria/associados/estado/{estado}/'
        driver.get(url)
        print(f'Acessando: {url}')
        
        # Chamar a função de rolagem
        scroll_until_all_items_loaded(driver)
        
        visited_links = set()
        
        while True:
            try:
                # Localiza todos os elementos de link desejados na página
                links = driver.find_elements(By.CSS_SELECTOR, 'a.btn.btn-xs.btn-default.text-xs.text-uppercase')
                
                if not links:
                    break
                
                new_links = [link for link in links if link.get_attribute('href') not in visited_links]
                
                if not new_links:
                    break
                
                for link in new_links:
                    try:
                        href = link.get_attribute('href')
                        visited_links.add(href)
                        all_links.add(href)
                        
                        print(f'Clicando no link: {link.text}')
                        link.click()
                        
                        # Aguarde um pouco após o clique para garantir que a ação seja completada
                        time.sleep(5)  # Ajuste o tempo conforme necessário
                        
                        # Voltar para a página anterior
                        driver.back()
                        
                        # Aguarde o carregamento da página após voltar
                        time.sleep(5)  # Ajuste o tempo conforme necessário
                        
                        # Chamar a função de rolagem novamente, pois ao voltar a página a rolagem pode ser necessária
                        scroll_until_all_items_loaded(driver)
                    
                    except Exception as e:
                        print(f'Erro ao clicar no link: {e}')
            
            except Exception as e:
                print(f'Erro ao localizar links: {e}')
                break

    # Salva todos os links em um arquivo CSV após processar todas as páginas
    save_to_csv('paragrafos_extraidos.csv', all_links)

finally:
    driver.quit()
    print("Navegação concluída.")
