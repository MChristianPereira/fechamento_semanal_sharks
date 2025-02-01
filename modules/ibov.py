import pandas as pd
import plotly.graph_objects as go

class ibov:
    def __init__(self):
         
         self.ibov = pd.read_parquet('archives/ibov.parquet')

    def iniciar_script_main(self):

        self.definindo_layout()
        self.grafico_ibov()

    def definindo_layout(self):

        self.layout = go.Layout(
            paper_bgcolor = '#FAFAFA',
            plot_bgcolor = '#FAFAFA',
            xaxis = dict(showgrid = False,
                        tickfont = dict (size = 20),
                        tickformat="%m/%y",
                        linecolor = 'black'
                        ),
            font = dict(family = 'Avenir Next LT Pro',
                        color = '#000000'),
            yaxis = dict(showgrid = False,
                        tickfont = dict (size = 20),
                        tickformat = '.',
                        linecolor = 'black',
                        ),
            margin = dict (l = 800,
                           r = 800,
                           b = 300,
                           t = 300),
        )

    def grafico_ibov(self):
        fig = go.Figure (layout = self.layout)

        fig.add_trace (
            go.Scatter(
                y = self.ibov['fechamento'],
                x = self.ibov['data'],
                mode = 'lines',
                name = 'IBOV',
                marker_color = '#245CA6',
                line=dict(width = 5)))

        fig.write_image("archives/ibov.png", height = 1182, width = 2384)

if __name__ == '__main__':
    ibov()