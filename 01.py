from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

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

try:
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
finally:
    driver.quit()
    print("Navegação concluída.")
