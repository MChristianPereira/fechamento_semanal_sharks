import requests
import pandas as pd
import os
import urllib.request

class dados_fintz:

    def __init__(self):

        self.chave_api = os.getenv("API_FINTZ")
        self.headers = {'accept': 'application/json', 'X-API-Key': self.chave_api}

    def iniciar_script_main(self):

        print('Iniciando a coleta de dados na Fintz...')
        self.ibov()
        self.pegar_cotacoes()

    def ibov(self):

        data_inicial = '2024-01-01'
        url = f'https://api.fintz.com.br/indices/historico?indice=IBOV&dataInicio={data_inicial}'
        response = requests.get(url, headers = self.headers)

        df = pd.DataFrame(response.json())
        df = df.sort_values('data', ascending=True)
        df.columns = ['indice', 'data', 'fechamento']
        df = df.drop('indice', axis = 1)
        df.to_parquet('archives/ibov.parquet', index = False)

    def pegar_cotacoes(self):       

        url = 'https://api.fintz.com.br/bolsa/b3/avista/cotacoes/historico/arquivos?classe=ACOES&preencher=true'
        response = requests.get(url, headers = self.headers)

        link_download = (response.json())['link']
        urllib.request.urlretrieve(link_download, f'archives/cotacoes.parquet')

        df = pd.read_parquet('archives/cotacoes.parquet')
        colunas_pra_ajustar = ['preco_abertura', 'preco_maximo', 'preco_medio', 'preco_minimo']

        for coluna in colunas_pra_ajustar:
            df[f'{coluna}_ajustado'] = df[coluna] * df['fator_ajuste']

        df['preco_fechamento_ajustado'] = df.groupby('ticker')['preco_fechamento_ajustado'].transform('ffill')
        df = df.sort_values('data', ascending=True)

        df.to_parquet('archives/cotacoes.parquet', index = False) 

if __name__ == "__main__":

    dados_fintz().ibov()
    dados_fintz().pegar_cotacoes()