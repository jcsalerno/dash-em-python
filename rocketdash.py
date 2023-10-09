# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_auth

USUARIOS = {
    "Julio": "Julio",
    "Login": "Login",
}

app = Dash(__name__)
auth = dash_auth.BasicAuth(app, USUARIOS)

#como funciona a dash 

#layout - HTML -> TEXTOS, IMAGENS, ESPAÇOS
#""""   - Dash Components (Core Components) -> gráficos, botões que mexem os gráficos, coisas da dashboard. 
#Callbacks - 
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")

#df = tabela = dataframe

# plotly = criação do gráfico
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
fig2 = px.scatter(df, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário", size_max=60)

#lista_marcas = ["Treinamentos", "Programação", "Todas"]
lista_marcas = list(df["Marca"].unique())
lista_marcas.append("Todas")

lista_paises = list(df["País"].unique())
lista_paises.append("Todos")

#css-layout
app.layout = html.Div(children=[
    html.H1(children='Meu Dashboard'),

    html.Div(children='''
        Dashboard de Vendas em Python
    '''),
    
    html.H3(children="Vendas de cada Produto por Loja", id="subtitulo"),
    
    dcc.RadioItems(options=lista_marcas, value="Todas", id='selecao_marcas'),
    html.Div(children=[
        dcc.Dropdown(options=lista_paises, value="Todos", id='selecao_pais'),
    ], style={"width": "50%", "margin": "auto"}),
    
    dcc.Graph(id='vendas_por_loja',figure=fig),
    dcc.Graph(id='distribuicao_vendas', figure=fig2),
    
    
], style={"text-align": "center"})


@app.callback(
    Output('selecao_pais', 'options'),
    Input ('selecao_marcas', 'value'),
)

def opcoes_pais(marca):
    #criar uma logica que diga qual a lista de países que ele vai pegar
    if marca == "Todas":
        nova_lista_paises = list(df["País"].unique())
        nova_lista_paises.append("Todos")
    else:
        df_filtrada = df.loc[df['Marca']==marca, :]
        nova_lista_paises = list(df_filtrada["País"].unique())
        nova_lista_paises.append("Todos")   
    return nova_lista_paises

#callbacks -> dar funcionalidade para dashboard (noncecta os botões com os gŕaficos )
@app.callback(
    Output('subtitulo', 'children'), #quem eu quero modificar (botão que o input modifique)
    Output('vendas_por_loja', 'figure'),
    Output('distribuicao_vendas', 'figure'),
    Input('selecao_marcas', 'value'), #quem está modificando / de onde eu quero pegar a informação / filtro
    Input('selecao_pais', 'value'),
)
def selecionar_marca(marca, pais):
    if marca == "Todas" and pais == "Todos":
        texto = "Vendas de cada Produto por Loja"
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
        fig2 = px.scatter(df, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário", size_max=60)
    else:
        df_filtrada = df
        if marca != "Todas":
            #filtrar de acordo com a marca
            df_filtrada = df_filtrada.loc[df_filtrada['Marca']==marca, :]
        if pais != "Todos":
            # filtrar de acordo com o pais
            df_filtrada = df_filtrada.loc[df_filtrada["País"]==pais, :]
        
        texto = f"Vendas de cada Produto por Loja da Marca {marca} e do País {pais}"
        fig = px.bar(df_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
        fig2 = px.scatter(df_filtrada, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário", size_max=60)
    return texto, fig, fig2


# colocando o seu site (seu dashboard) no ar
if __name__ == '__main__':
    app.run_server(debug=True)
