import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Leitura e preparação dos dados
df = pd.read_csv('ecommerce_estatistica.csv')

# Conversão das colunas numéricas
for coluna in ['Nota', 'N_Avaliações', 'Desconto', 'Preço']:
    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')


# Gráfico 1: Histograma dos preços
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

# 3. Gráfico 2: Dispersão
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

# Gráfico 3: Mapa de calor
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

# Gráfico 4: Barras
genero = df['Gênero'].value_counts().reset_index()
genero.columns = ['Gênero', 'Quantidade']

fig4 = px.bar(
    genero,
    x='Gênero',
    y='Quantidade',
    title='Quantidade de Produtos por Gênero',
    color_discrete_sequence=['orange']
)

fig4.update_layout(
    xaxis_title='Gênero',
    yaxis_title='Quantidade de Produtos'
)

# Gráfico 5: Pizza
qtd_vendidos = df['Qtd_Vendidos'].value_counts().reset_index()
qtd_vendidos.columns = ['Faixa de Vendas', 'Quantidade']

fig5 = px.pie(
    qtd_vendidos,
    names='Faixa de Vendas',
    values='Quantidade',
    title='Distribuição dos Produtos por Faixa de Vendas',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Gráfico 6: Densidade
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

# Gráfico 7: Regressão
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
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6),
    dcc.Graph(figure=fig7)

], style={'maxWidth': '1200px', 'margin': 'auto'})

# Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True, port=8050)
