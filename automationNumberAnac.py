from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Caminho para o driver do Chrome
path_to_chromedriver = './chromedriver.exe' # atualize isso para o caminho do seu chromedriver

# Inicializa o serviço do WebDriver
service = Service(path_to_chromedriver)

# Inicializa o driver do navegador
driver = webdriver.Chrome(service=service)

# Abre a página da web
driver.get('https://sistemas.anac.gov.br/educator/Index2.aspx')

# Encontra o botão e clica nele
botao = driver.find_element(By.ID, 'ContentPlaceHolder1_Button1')
botao.click()

# Abre o arquivo .txt para escrita
with open('keys.txt', 'w') as f:
    # Agora você pode continuar a raspagem de dados como antes
    for i in range(66):
        elemento = driver.find_element(By.ID, 'ContentPlaceHolder1_DataList1_Cod_EscolaLabel_'+str(i))
        print(elemento.text)

        # Escreve o resultado no arquivo .txt
        f.write(elemento.text + '\n')

# Lembre-se de fechar o driver quando terminar
driver.quit()
