from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
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

    # Iterar sobre os elementos e clicar em cada um
    for i, elemento in enumerate(elementos):
        print(f"Clicando no elemento {i + 1}/{len(elementos)}...")

        # Clicar no elemento
        elemento.click()
        time.sleep(5)  # Aguardar 5 segundos para garantir que a informação carregue

        # Clicar no botão de fechar do pop-up
        fechar_popup = driver.find_element(By.CSS_SELECTOR, "div.jet-popup__close-button")
        driver.execute_script("arguments[0].scrollIntoView();", fechar_popup)
        fechar_popup.click()
        time.sleep(1)
        
        print(f"pop")

except Exception as e:
    print("Erro ao capturar dados:", e)

finally:
    # Salvar os dados em um arquivo JSON
    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    # Criar um DataFrame com os dados
    df = pd.DataFrame(dados)
    df.to_csv("dados.csv", index=False, encoding='utf-8')

    # Fechar o navegador
    driver.quit()
