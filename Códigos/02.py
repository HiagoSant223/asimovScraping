from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

# Configuração do Firefox em modo headless
options = Options()
options.headless = False  # Defina como True para modo headless
driver = webdriver.Firefox(options=options)

try:
    # Acessar o site
    driver.get("https://abrape.com.br/associados/?jsf=jet-engine:lista&tax=estado:286")
    
    dados = []

    # Aguarde alguns segundos para garantir que a página carregue
    time.sleep(5)

    # Identificar todos os elementos div com a classe especificada
    elementos = driver.find_elements(By.CSS_SELECTOR, "div.elementor.elementor-327")
    print(f"Quantidade de elementos encontrados: {len(elementos)}")

    for i, elemento in enumerate(elementos):
        print(f"Clicando no elemento {i + 1}/{len(elementos)}...")

        # Clicar no elemento
        elemento.click()
        time.sleep(5)  # Aguardar 5 segundos para garantir que a informação carregue

        # Capturar o HTML da página atual
        html_completo = driver.page_source
        
        # Usar BeautifulSoup para extrair as informações desejadas
        soup = BeautifulSoup(html_completo, 'html.parser')
        
        # Função para obter todos os textos com um seletor
        def get_all_texts(selector):
            elements = soup.select(selector)
            return [el.text.strip() for el in elements]

        # Capturar as informações
        nomes = get_all_texts('div.elementor-widget-container p.elementor-heading-title')
        
        # Atribuir valores às variáveis
        nome = nomes[0] if len(nomes) > 0 else ''
        slogan = nomes[1] if len(nomes) > 1 else ''
        telefone1 = nomes[2] if len(nomes) > 2 else ''
        telefone2 = nomes[3] if len(nomes) > 3 else ''

        # Obter o e-mail e extrair apenas a parte antes do ?
        email_tag = soup.select_one('a[href^="mailto:"]')
        email = email_tag.get('href', '').replace('mailto:', '') if email_tag else ''
        email = email.split('?')[0]  # Mantém apenas a parte antes do '?'
        
        # Extrair os links corretamente
        site = soup.select_one('a[href^="http"]').get('href', '') if soup.select_one('a[href^="http"]') else ''
        facebook = soup.select_one('a.elementor-social-icon-facebook').get('href', '') if soup.select_one('a.elementor-social-icon-facebook') else ''
        instagram = soup.select_one('a.elementor-social-icon-instagram').get('href', '') if soup.select_one('a.elementor-social-icon-instagram') else ''

        # Adicionar ao dicionário sem o HTML
        dados.append({
            'Nome': nome,
            'Slogan': slogan,
            'Telefone 1': telefone1,
            'Telefone 2': telefone2,
            'E-mail': email,
            'Site': site,
            'Facebook': facebook,
            'Instagram': instagram
        })

        # Clicar no botão de fechar do pop-up
        fechar_popup = driver.find_element(By.CSS_SELECTOR, "div.jet-popup__close-button")
        fechar_popup.click()
        time.sleep(1)

except Exception as e:
    print("Erro ao capturar dados:", e)

finally:
    # Criar um DataFrame com os dados
    df = pd.DataFrame(dados)
    
    # Salvar em CSV
    df.to_csv("dados_extraidos.csv", sep=';', index=False, encoding='utf-8')
    
    # Salvar em JSON sem o HTML
    with open("dados_extraidos.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    # Fechar o navegador
    driver.quit()
