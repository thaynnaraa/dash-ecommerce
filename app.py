```python
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Leitura e preparação dos dados
df = pd.read_csv('ecommerce_estatistica.csv')

# Conversão das colunas numéricas
for coluna in ['Nota', 'N_Avaliações', 'Desconto', 'Preço']:
    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')


# Gráfico 1: Histograma - Distribuição dos preços
fig1 = px.histogram(
    df,
    x='Preço',
    nbins=20,
    title='Distribuição dos Preços dos Produtos',
    color_discrete_sequence=['green']
)

fig1.update_layout(
    xaxis_title='Preço (R$)',
    yaxis_title='Quantidade de Produtos'
)

# 3. Gráfico 2: Dispersão - Relação entre preço e número de avaliações
fig2 = px.scatter(
    df,
    x='Preço',
    y='N_Avaliações',
    title='Relação entre Preço e Número de Avaliações dos Produtos',
    color_discrete_sequence=['blue'],
    opacity=0.8
)

fig2.update_layout(
    xaxis_title='Preço (R$)',
    yaxis_title='Número de Avaliações'
)

# Gráfico 3: Mapa de calor - Correlação entre variáveis numéricas
correlacao = df[
    ['Nota', 'N_Avaliações', 'Desconto', 'Preço']
].corr()

fig3 = px.imshow(
    correlacao,
    text_auto='.2f',
    color_continuous_scale='RdBu_r',
    title='Mapa de Calor da Correlação entre as Variáveis',
    zmin=-1,
    zmax=1
)

# Gráfico 4: Barras - Preço médio por marca
preco_marca = df.groupby('Marca')['Preço'].mean().reset_index()

preco_marca = preco_marca.sort_values(
    by='Preço', ascending=False
).head(10)

fig4 = px.bar(
    preco_marca,
    x='Marca',
    y='Preço',
    title='Preço Médio dos Produtos por Marca',
    color_discrete_sequence=['orange']
)

fig4.update_layout(
    xaxis_title='Marca',
    yaxis_title='Preço Médio (R$)'
)

# Gráfico 5: Pizza - Distribuição por faixa de vendas
qtd_vendidos = df['Qtd_Vendidos'].value_counts().reset_index()
qtd_vendidos.columns = ['Faixa de Vendas', 'Quantidade']

fig5 = px.pie(
    qtd_vendidos,
    names='Faixa de Vendas',
    values='Quantidade',
    title='Distribuição dos Produtos por Faixa de Vendas',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Gráfico 6: Densidade - Concentração dos preços
fig6 = px.histogram(
    df,
    x='Preço',
    nbins=30,
    histnorm='probability density',
    title='Distribuição dos Preços dos Produtos',
    color_discrete_sequence=['purple']
)

fig6.update_layout(
    xaxis_title='Preço (R$)',
    yaxis_title='Densidade'
)

# Gráfico 7: Regressão - Tendência entre preço e número de avaliações
fig7 = px.scatter(
    df,
    x='Preço',
    y='N_Avaliações',
    trendline='ols',
    title='Regressão entre Preço e Número de Avaliações',
    color_discrete_sequence=['green'],
    opacity=0.6,
    trendline_color_override='red'
)

fig7.update_layout(
    xaxis_title='Preço (R$)',
    yaxis_title='Número de Avaliações'
)

# Criação do dashboard
app = Dash(__name__)

app.layout = html.Div([

    html.H1(
        'Dashboard de E-commerce',
        style={'textAlign': 'center'}
    ),

    html.P(
        'Análise dos dados dos produtos por meio de gráficos estatísticos.',
        style={'textAlign': 'center'}
    ),

    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    
    html.H3('4. Preço Médio dos Produtos por Marca'),
    
    dcc.Label('Selecione uma marca:'),
    
    dcc.Dropdown(
        id='filtro-marca',
        options=[
            {'label': 'Todas as marcas', 'value': 'Todas'}
        ] + [
            {'label': marca, 'value': marca}
            for marca in df['Marca'].dropna().unique()
        ],
        value='Todas',
        clearable=False
    ),
    
    dcc.Graph(id='grafico4', figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6),
    dcc.Graph(figure=fig7)
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6),
    dcc.Graph(figure=fig7)

], style={'maxWidth': '1200px', 'margin': 'auto'})

# Filtro interativo do gráfico 4

@app.callback(
    Output('grafico4', 'figure'),
    Input('filtro-marca', 'value')
)
def atualizar_grafico4(marca):

    if marca == 'Todas':
        dados = df.groupby('Marca')['Preço'].mean().reset_index()

        dados = dados.sort_values(
            by='Preço', ascending=False
        ).head(10)

    else:
        dados = df[df['Marca'] == marca]

        dados = dados.groupby('Marca')['Preço'].mean().reset_index()

    fig = px.bar(
        dados,
        x='Marca',
        y='Preço',
        title='Preço Médio dos Produtos por Marca',
        color_discrete_sequence=['orange']
    )

    fig.update_layout(
        xaxis_title='Marca',
        yaxis_title='Preço Médio (R$)'
    )

    return fig

# Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True, port=8050)
```
