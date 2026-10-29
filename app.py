import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# 1. Leitura e preparação dos dados
df = pd.read_csv('ecommerce_estatistica.csv')

for coluna in ['Preço', 'Nota', 'N_Avaliações']:
    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

df = df.dropna(subset=['Preço', 'Nota'])

# Paletas de cores
CORES = px.colors.qualitative.Set2
CORES_VIVAS = px.colors.qualitative.Bold

def cria_graficos(filtro_genero):

    # 2. Filtragem dos dados
    if filtro_genero == 'Todos':
        dados = df.copy()
    else:
        dados = df[df['Gênero'] == filtro_genero].copy()

    # Gráfico 1: Histograma de preços
    fig1 = px.histogram(
        dados,
        x='Preço',
        nbins=30,
        title='Distribuição dos Preços',
        color_discrete_sequence=[CORES[0]]
    )

    fig1.update_layout(
        xaxis_title='Preço',
        yaxis_title='Quantidade de Produtos'
    )

    # Gráfico 2: Pizza das 8 marcas mais frequentes
    marcas = dados['Marca'].fillna('Não informado')
    contagem = marcas.value_counts()
    principais = contagem.head(8)

    fig2 = px.pie(
        names=principais.index,
        values=principais.values,
        title='8 Marcas com Mais Produtos',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Gráfico 3: Bolhas
    bolhas = dados.dropna(
        subset=['Nota', 'Preço', 'N_Avaliações', 'Gênero']
    )

    fig3 = px.scatter(
        bolhas,
        x='Nota',
        y='Preço',
        size='N_Avaliações',
        color='Gênero',
        title='Preço e Nota dos Produtos',
        color_discrete_map={
            'Masculino': '#1f77b4',
            'Feminino': '#e377c2',
            'Sem gênero': '#7f7f7f',
            'Meninos': '#17becf',
            'Meninas': '#bcbd22',
            'Sem gênero infantil': '#9467bd',
            'Bebês': '#ff7f0e',
            'Unissex': '#2ca02c',
            'roupa para gordinha pluss P ao 52': '#d62728'
        }
    )

    fig3.update_layout(
        xaxis_title='Nota',
        yaxis_title='Preço',
        legend_title='Gênero'
    )

    # Gráfico 4: Linha com preço médio por nota
    linha = dados.groupby('Nota')['Preço'].mean().reset_index()
    linha = linha.sort_values('Nota')

    fig4 = px.line(
        linha,
        x='Nota',
        y='Preço',
        title='Preço Médio por Nota',
        color_discrete_sequence=[CORES_VIVAS[1]]
    )

    fig4.update_layout(
        xaxis_title='Nota',
        yaxis_title='Preço Médio'
    )

    # Gráfico 5: Visualização 3D
    dados3d = dados.dropna(
        subset=['Preço', 'Nota', 'N_Avaliações', 'Temporada']
    )

    fig5 = px.scatter_3d(
        dados3d,
        x='Preço',
        y='Nota',
        z='N_Avaliações',
        color='Temporada',
        title='Visualização 3D dos Produtos',
        color_discrete_sequence=px.colors.qualitative.Dark24
    )

    fig5.update_layout(
        scene=dict(
            xaxis_title='Preço',
            yaxis_title='Nota',
            zaxis_title='Número de Avaliações'
        ),
        legend_title='Temporada'
    )

    # Gráfico 6: Barras das 10 marcas com mais produtos
    marcas = dados['Marca'].fillna('Não informado')
    contagem_marcas = marcas.value_counts()
    top_marcas = contagem_marcas.head(10).index

    barras = dados.copy()
    barras['Marca'] = barras['Marca'].fillna('Não informado')
    barras = barras[barras['Marca'].isin(top_marcas)]

    media_marcas = barras.groupby('Marca')['Preço'].mean().reset_index()
    media_marcas = media_marcas.sort_values('Preço', ascending=False)

    fig6 = px.bar(
        media_marcas,
        x='Marca',
        y='Preço',
        title='Preço Médio das 10 Principais Marcas',
        color='Marca',
        color_discrete_sequence=CORES_VIVAS
    )

    fig6.update_layout(
        xaxis_title='Marca',
        yaxis_title='Preço Médio',
        showlegend=False
    )

    return fig1, fig2, fig3, fig4, fig5, fig6

# 3. Criação do dashboard
app = Dash(__name__)

generos = df['Gênero'].dropna().unique().tolist()
generos.sort()

opcoes_genero = [
    {'label': 'Todos os gêneros', 'value': 'Todos'}
]

for genero in generos:
    opcoes_genero.append({
        'label': genero,
        'value': genero
    })

app.layout = html.Div([
    html.H1(
        'Dashboard de E-commerce',
        style={'textAlign': 'center'}
    ),

    html.P(
        'Explore os dados dos produtos usando o filtro de gênero.',
        style={'textAlign': 'center'}
    ),

    html.Label('Selecione o gênero:'),

    dcc.Dropdown(
        id='filtro-genero',
        options=opcoes_genero,
        value='Todos',
        clearable=False
    ),

    dcc.Graph(id='grafico-histograma'),
    dcc.Graph(id='grafico-pizza'),
    dcc.Graph(id='grafico-bolhas'),
    dcc.Graph(id='grafico-linha'),
    dcc.Graph(id='grafico-3d'),
    dcc.Graph(id='grafico-barras')

], style={'maxWidth': '1200px'})

# 4. Atualização dos gráficos pelo filtro
@app.callback(
    [
        Output('grafico-histograma', 'figure'),
        Output('grafico-pizza', 'figure'),
        Output('grafico-bolhas', 'figure'),
        Output('grafico-linha', 'figure'),
        Output('grafico-3d', 'figure'),
        Output('grafico-barras', 'figure')
    ],
    Input('filtro-genero', 'value')
)
def atualiza_graficos(filtro_genero):
    return cria_graficos(filtro_genero)

# 5. Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True, port=8050)
