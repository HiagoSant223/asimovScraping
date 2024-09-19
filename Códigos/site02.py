from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

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

            for p in p_tags:
                print(p.text)
            
            for a in a_tags:
                print(a.text, a.get_attribute('href'))
            
            driver.back()
            time.sleep(5)

        except Exception as e:
            print(f'Erro ao clicar no elemento: {e}')
    else:
        print("Nenhum elemento encontrado.")

finally:
    driver.quit()
    print("Navegação concluída.")
