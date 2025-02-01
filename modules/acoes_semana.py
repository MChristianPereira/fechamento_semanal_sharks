import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

class DadosNaoAtualizadosError(Exception):
    pass

class acoes_semana():
    def __init__(self):

        self.cotacoes = pd.read_parquet('archives/cotacoes.parquet')
        
        data_carteira_ibov = datetime.now().date()
        if data_carteira_ibov.weekday() == 5:
            data_carteira_ibov += timedelta(days = 2)
        elif data_carteira_ibov.weekday() == 6:
            data_carteira_ibov += timedelta(days = 1)
        else:
            data_carteira_ibov = data_carteira_ibov

        data_carteira_ibov = data_carteira_ibov.strftime('%d-%m-%y')

        self.carteira_ibov = f"IBOVDia_{data_carteira_ibov}.csv"

    def iniciar_script_main(self):

        print("Iniciando o script...")
        self.definindo_periodo()
        self.verificando_dados_parquet()
        self.filtrando_dados()
        self.calculando_retorno_semanal()
        acoes_alta, acoes_queda = self.ranking_acoes()
        self.definindo_layout()
        self.gerando_grafico(acoes_alta, acoes_queda)

    def definindo_periodo(self):

        data_final = datetime.now().date()# - timedelta(days = 1)
        if data_final.weekday() == 5:
            data_final = (data_final - timedelta(days=1))
        elif data_final.weekday() == 6:
            data_final = (data_final - timedelta(days=2))
        else:
            data_final = data_final

        data_inicial = data_final - timedelta(days = 7)
        self.data_inicial = data_inicial.strftime("%Y-%m-%d")
        self.data_final = data_final.strftime("%Y-%m-%d")

    def verificando_dados_parquet(self):

        data_final_cotacoes = self.cotacoes['data'].iloc[-1]
        data_final = pd.to_datetime(self.data_final)
        condicao = data_final == data_final_cotacoes

        if condicao == False:
            raise DadosNaoAtualizadosError("Os dados não foram atualizados")

    def filtrando_dados(self):

        carteira_ibov = pd.read_csv(f'archives/{self.carteira_ibov}', encoding = 'latin1', sep = ';', engine = 'python', header = 1, index_col = False, skipfooter = 2)
        carteira_ibov = carteira_ibov['Código'].to_frame()
        cotacoes = self.cotacoes[self.cotacoes['ticker'].isin(carteira_ibov['Código'])]
        cotacoes = cotacoes[['data', 'ticker', 'preco_fechamento_ajustado']]
        self.cotacoes = cotacoes[(cotacoes['data'] == self.data_inicial) | (cotacoes['data'] == self.data_final)]

    def calculando_retorno_semanal(self):

        cotacoes = self.cotacoes.sort_values(['ticker', 'data'])
        cotacoes['Retorno Semanal'] = cotacoes.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
        self.cotacoes = cotacoes.set_index('ticker')['Retorno Semanal']

    def ranking_acoes(self):

        cotacoes = self.cotacoes

        acoes_alta = cotacoes.sort_values(ascending = False)
        acoes_alta = acoes_alta[0:5]
        acoes_alta = acoes_alta.iloc[::-1]

        acoes_queda = cotacoes.sort_values(ascending = True)
        acoes_queda = acoes_queda[0:5]

        return acoes_alta, acoes_queda

    def definindo_layout(self):

        self.layout = go.Layout(
            paper_bgcolor = '#FAFAFA',
            plot_bgcolor = '#FAFAFA',
            yaxis = dict(showgrid = False,
                        tickfont = dict(size = 24),
                        range = [-0.75, 9.5]),
            font = dict(family = 'Avenir Next LT Pro',
                        color = '#000000'),
            xaxis = dict(showgrid = False,
                        tickfont = dict(size = 26),
                        tickformat = '.0%',
                        range = [-0.5, 0.5],
                        visible = False),
            margin = dict(l = 600,
                        r = 600,
                        b = 100,
                        t = 100),
            bargap = 0.1
        )

    def gerando_grafico(self, df1, df2):

        acoes_alta = df1
        acoes_queda = df2
        lista_df = [acoes_queda, acoes_alta]

        fig = go.Figure(layout = self.layout)

        for i, df in enumerate(lista_df):

            cor = 'green' if i == 1 else 'red'

            fig.add_trace(
                go.Bar(
                    x = df.values,
                    y = df.index,
                    width = 0.4,
                    orientation = 'h',
                    marker_color = cor,
                    text = [f'{val:.2%}' for val in df.values],
                    textfont = dict(size = 20, color = '#000000'),
                    textposition = 'outside',
                    showlegend = False
                )
            )

        fig.add_shape(
            type = "line",
            x0 = 0, y0 = -0.5,
            x1 = 0, y1 = 9.5,
            line = dict(color = "#000000", width = 2)
        )

        fig.write_image("archives/fechamento_semanal_acoes.png", height = 1182, width = 2384)

if __name__ == '__main__':
    acoes_semana().iniciar_script_main()
    # try:
    #     acoes_semana().iniciar_script_main()
    # except DadosNaoAtualizadosError as e:
    #     print(f"Erro: {e}")