from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import json

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

try:
    url = 'https://abrape.com.br/associados/?jsf=jet-engine:lista&tax=estado:263'
    driver.get(url)
    print(f'Acessando: {url}')
    
    time.sleep(5)

    elements = driver.find_elements(By.CSS_SELECTOR, 'div.elementor.elementor-327')
    
    if elements:
        first_element = elements[0]
        try:
            print(f'Clicando no elemento: {first_element.text}')
            first_element.click()
            
            time.sleep(5)

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

            for a in a_tags:
                href = a.get_attribute('href')
                if 'facebook.com' in href:
                    facebook = href
                elif 'instagram.com' in href:
                    instagram = href
                elif 'mailto:' in href:
                    email = href.split(':')[1].split('?')[0]  # Captura apenas o e-mail
                elif site == '':  # Se não tiver um site capturado ainda
                    site = href

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

            df = pd.DataFrame(data, index=[0])
            print(df)

            # Salvando em um arquivo JSON
            with open('dados.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)

            print("Dados salvos em 'dados.json'.")

            driver.back()
            time.sleep(5)

        except Exception as e:
            print(f'Erro ao clicar no elemento: {e}')
    else:
        print("Nenhum elemento encontrado.")

finally:
    driver.quit()
    print("Navegação concluída.")
