# Dashboard de E-commerce

## Sobre o projeto

Este projeto foi desenvolvido como atividade de estudo de análise de dados. O objetivo é apresentar informações de um conjunto de dados de produtos de e-commerce por meio de gráficos interativos.

## Tecnologias utilizadas

- Python
- Pandas
- Plotly
- Dash
- Scipy
- Statsmodels

## Gráficos disponíveis

O dashboard apresenta sete gráficos:

1. **Histograma:** apresenta a distribuição dos preços dos produtos.
2. **Gráfico de dispersão:** demonstra a relação entre o preço dos produtos e o número de avaliações.
3. **Mapa de calor:** apresenta a correlação entre as variáveis numéricas Nota, N_Avaliações, Desconto e Preço.
4. **Gráfico de barras:** compara o preço médio dos produtos por marca, destacando inicialmente as dez marcas com maior preço médio.
5. **Gráfico de pizza:** apresenta a distribuição dos produtos por faixa de vendas (`Qtd_Vendidos`).
6. **Gráfico de densidade:** apresenta a distribuição dos preços em escala de densidade, permitindo observar sua concentração.
7. **Gráfico de regressão:** demonstra a tendência da relação entre preço e número de avaliações dos produtos.

## Interatividade

O dashboard possui um filtro interativo por marca no gráfico de barras. É possível selecionar uma marca específica para visualizar seu preço médio ou escolher a opção "Todas as marcas" para visualizar as dez marcas com maior preço médio.

A atualização do gráfico é realizada por meio de um callback do Dash (`@app.callback`).

## Arquivos do projeto

- `app.py`: código da aplicação e dos gráficos.
- `ecommerce_estatistica.csv`: conjunto de dados utilizado.
- `requirements.txt`: bibliotecas necessárias para executar o projeto.

## Como executar o projeto

1. Instale as bibliotecas listadas no arquivo `requirements.txt`:

   `pip install -r requirements.txt`

2. Execute o arquivo `app.py`:

   `python app.py`

3. Abra o endereço indicado no terminal em um navegador. Por padrão, a aplicação é executada em `http://127.0.0.1:8050`.

## Observação

Este projeto foi desenvolvido para fins de aprendizado e prática de análise e visualização de dados com Python.
