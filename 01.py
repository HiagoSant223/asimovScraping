from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import json
import csv

# Lista de estados
estados = [
    'sao-paulo' # Adicione mais estados conforme necessário
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

def process_page_for_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Garante que a requisição foi bem-sucedida
        
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.select_one('div.entry-content')

        if content_div:
            paragraphs = content_div.select('p')
            return [p.text.strip() for p in paragraphs]
        else:
            print(f'Conteúdo não encontrado para a URL: {url}')
            return None
    except requests.RequestException as e:
        print(f'Erro ao requisitar a URL: {e}')
        return None

def save_to_json(file_name, links):
    try:
        data = []
        for link in links:
            page_data = process_page_for_json(link)
            if page_data:
                data.append(page_data)
        
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)  # Salva com indentação para ficar mais legível
        
    except IOError as e:
        print(f'Erro ao escrever no arquivo JSON: {e}')

def replace_newlines(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if isinstance(data[i][j], str):  # Verifica se é uma string
                data[i][j] = data[i][j].replace("\\n", "\n")
    return data

def json_to_csv(json_file, csv_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Substituir \n por quebras de linha reais
        data = replace_newlines(data)
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Texto'])  # Cabeçalho do CSV
            
            for page in data:
                for paragraph in page:
                    writer.writerow([paragraph])
    
    except IOError as e:
        print(f'Erro ao acessar os arquivos: {e}')

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

    # Salva todos os dados em um arquivo JSON após processar todas as páginas
    save_to_json('SãoPaulo.json', all_links)

finally:
    driver.quit()
    print("Navegação concluída.")
    
# Converte o arquivo JSON para CSV
json_to_csv('SãoPaulo.json', 'SãoPaulo.csv')
