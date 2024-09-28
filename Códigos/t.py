from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import json

# Configurações do Selenium
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

try:
    url = 'https://abrape.com.br/associados/?jsf=jet-engine:lista&tax=estado:286'
    
    all_data = []  # Lista para armazenar os dados coletados
    
    # Acessa a página para capturar os elementos inicialmente
    driver.get(url)
    print(f'Acessando: {url}')
    time.sleep(10)

    # Captura os elementos da página
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.elementor.elementor-327')
    total_items = len(elements)
    print(f'Itens encontrados na página: {total_items}')
    
    if total_items > 0:
        # Itera sobre os elementos usando seus índices
        for index in range(total_items):
           
            time.sleep(10)

            if index < len(elements):  # Verifica se o índice é válido
                element = elements[index]
                try:
                    print(f'[{index + 1}/{total_items}] Clicando no elemento: {element.text}')
                    element.click()  # Clica no item atual
                    
                    time.sleep(10)

                    # Coleta as informações da nova página
                    target_div = driver.find_element(By.CSS_SELECTOR, 'div.elementor-column.elementor-col-50.elementor-top-column.elementor-element.elementor-element-7864a13')
                    
                    p_tags = target_div.find_elements(By.TAG_NAME, 'p')
                    a_tags = target_div.find_elements(By.TAG_NAME, 'a')

                    nome = p_tags[0].text if len(p_tags) > 0 else ''
                    slogan = p_tags[1].text if len(p_tags) > 1 else ''
                    telefones = [p_tags[i].text for i in range(2, 4)] if len(p_tags) > 3 else ['', '']
                    email = ''
                    site = ''
                    facebook = ''
                    instagram = ''

                    # Captura os links (e-mail, redes sociais, etc.)
                    for a in a_tags:
                        href = a.get_attribute('href')
                        if 'facebook.com' in href:
                            facebook = href
                        elif 'instagram.com' in href:
                            instagram = href
                        elif 'mailto:' in href:
                            email = href.split(':')[1].split('?')[0]  # Extrai apenas o e-mail
                        elif site == '':  # Se não tiver um site capturado ainda
                            site = href

                    # Organiza os dados coletados
                    data = {
                        'Nome': nome,
                        'Slogan': slogan,
                        'Telefone 1': telefones[0],
                        'Telefone 2': telefones[1],
                        'E-mail': email,
                        'Site': site,
                        'Facebook': facebook,
                        'Instagram': instagram
                    }

                    # Adiciona os dados à lista geral
                    all_data.append(data)

                except Exception as e:
                    print(f'Erro ao clicar no elemento: {e}')
            else:
                print(f'Índice inválido: {index}')

    else:
        print("Nenhum elemento encontrado.")
    
    # Converte a lista de dados em um DataFrame e exibe
    df = pd.DataFrame(all_data)
    print(df)

    # Salva os dados em um arquivo JSON
    with open('dados.json', 'w') as json_file:
        json.dump(all_data, json_file, indent=4)

    print("Dados salvos em 'dados.json'.")

finally:
    # Encerra o navegador
    driver.quit()
    print("Navegação concluída.")