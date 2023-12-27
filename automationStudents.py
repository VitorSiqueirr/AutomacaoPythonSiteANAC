from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

# Caminho para o driver do Chrome
path_to_chromedriver = './chromedriver.exe' # atualize isso para o caminho do seu chromedriver

# Inicializa o serviço do WebDriver
service = Service(path_to_chromedriver)

# Inicializa o driver do navegador
driver = webdriver.Chrome(service=service)
df = pd.DataFrame()

# Abre a página da web
driver.get('https://sistemas.anac.gov.br/educator/Exames.Aspx')

# Lista de códigos das escolas
# keys = [171,212,244,123,1252,453,7,59,102,55,52,53,11,254,256,188,301,81,130,205,116,423,94,306,1216,1259,1038,548,39,425,1134,383,1007,1139,1111,1137,609,608,566,506,1104,1146,1092,1049,1053,445,430,1200,1069,1202,278,141,276,1236,1190,571,1149,233,1255,1253,494,540,1088,1251,1256,554]
# Lê as chaves de um arquivo .txt
with open('keys.txt', 'r') as f:
    keys = f.read().splitlines()

# Converte as chaves para inteiros
keys = [int(key) for key in keys]

for i in range(0, len(keys)):
    # Encontra o campo de código e insere o código da escola
    campo_codigo = driver.find_element(By.ID, 'ContentPlaceHolder1_Codigo')
    campo_codigo.clear()  # Limpa o campo antes de inserir um novo valor
    campo_codigo.send_keys(keys[i])  # Insere o código da escola

    # Clica no botão buscar
    botao_buscar = driver.find_element(By.ID, 'ContentPlaceHolder1_btnBuscar')
    botao_buscar.click()

    # Aguarda a página carregar
    time.sleep(5)

    # Coleta as informações de todos os alunos
    pagina = 1
    while True:
        # Extrai as informações da página atual
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Encontra a tabela
        tabela = soup.find('table', attrs={'id': 'ContentPlaceHolder1_grdResultado'})

        # Se a tabela existir, encontra todas as linhas e extrai os dados
        if tabela is not None:
            linhas = tabela.find_all('tr')

            for linha in linhas:
                # Encontra todas as células dentro da linha
                celulas = linha.find_all('td')

                # Extrai o texto de cada célula
                dados_aluno = [celula.text for celula in celulas]
                df = df._append(pd.Series(dados_aluno), ignore_index=True)
                print(dados_aluno)

        # Tenta encontrar o botão para a próxima página
        try:
            botao_proxima_pagina = driver.find_element(By.LINK_TEXT, str(pagina + 1))
        except NoSuchElementException:
            break

        # Clica no botão para a próxima página e aguarda a página carregar
        botao_proxima_pagina.click()
        time.sleep(5)
        pagina += 1

# Fecha o driver
driver.quit()

df.to_excel('dados_alunos.xlsx', index=False)
