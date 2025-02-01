import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def composicao_ibov():

    print('Iniciando a coleta da composição do Ibovespa')
    diretorio_atual = os.getcwd()
    diretorio_downloads = os.path.join(diretorio_atual, 'archives')

    for filename in os.listdir(diretorio_downloads):
        if filename.startswith("IBOVDia") and filename.endswith(".csv"):
            
            nome_arquivo_na_pasta = f"IBOVDia_{datetime.now().strftime('%d-%m-%y')}.csv"
            if filename == nome_arquivo_na_pasta:
                exit()

            arquivo_para_remover = os.path.join(diretorio_downloads, filename)
            os.remove(arquivo_para_remover)

    options = Options()
    options.headless = True
    options.add_argument('--headless')
    prefs = {
        "download.default_directory": diretorio_downloads,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    url = 'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
    driver.get(url)
    driver.implicitly_wait(5)
    
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "bvmf_iframe")))

    local_botao_download_csv = '/html/body/app-root/app-day-portfolio/div/div/div[1]/form/div[2]/div/div[2]/div/div/div[1]/div[2]/p/a'
    botao_download_csv = driver.find_element('xpath', local_botao_download_csv)
    driver.execute_script('arguments[0].click();', botao_download_csv)

    time.sleep(5)
    driver.quit()

if __name__ == '__main__':
    composicao_ibov()