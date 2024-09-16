import requests
from bs4 import BeautifulSoup

class Site: 
    def __init__(self, site):
        self.site = site
        self.news = []
        
    def updade_news(self):
        if self.size.lower() == 'globo':
            url = 'https://abrafesta.com.br/perfil-do-associado/hoteldall/'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
            page = requests.get(url, headers = browsers)
            
            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')
            
            soup.find_all('a')
            tg_class1 = ''
            