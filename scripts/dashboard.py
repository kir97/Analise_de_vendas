import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Conexão com o banco de dados SQLite
conect = sqlite3.connect("./data/dataset_vendas_ficticias.db")

# Carregar os dados
@st.cache
def carregar_dados():
    return pd.read_sql_query("SELECT * FROM registro_vendas;", conect)

df = carregar_dados()

# Calcular o faturamento e a margem de lucro
df["Faturamento"] = df["Quantidade Vendida"] * df["Preço Unitário"]
df["Margem de Lucro"] = (df["Preço Unitário"] - df["Custo Unitário"]) * df["Quantidade Vendida"]

# Calcular as vendas por mês
df["Data da Venda"] = pd.to_datetime(df["Data da Venda"])
df["Mês"] = df["Data da Venda"].dt.to_period("M")
vendas_mensais = df.groupby("Mês")["Faturamento"].sum()

# Gráficos interativos com Plotly

# Filtros de visualização
st.sidebar.header("Filtros")
produto_selecionado = st.sidebar.selectbox("Selecione o Produto", ['Todos'] + list(df["Produto"].unique()))
df_filtrado = df[(df["Produto"] == produto_selecionado) | (produto_selecionado == 'Todos')]

# Exibir KPIs
st.header("KPIs Importantes")
faturamento_total = df_filtrado['Faturamento'].sum()
margem_lucro_total = df_filtrado['Margem de Lucro'].sum()
st.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
st.metric("Margem de Lucro Total", f"R$ {margem_lucro_total:,.2f}")

# Gráfico de Faturamento Mensal
st.header("Faturamento Mensal")
vendas_mensais_df = vendas_mensais.reset_index()
vendas_mensais_df["Mês"] = vendas_mensais_df["Mês"].astype(str)
fig = px.line(vendas_mensais_df, x="Mês", y="Faturamento", title='Faturamento Mensal')
st.plotly_chart(fig)

# Gráfico de Vendas por Categoria
st.header("Vendas por Categoria")
vendas_categoria = df.groupby("Categoria")["Faturamento"].sum().reset_index()
fig = px.bar(vendas_categoria, x="Categoria", y="Faturamento", title="Vendas por Categoria")
st.plotly_chart(fig)

# Exibir relatório como CSV
st.download_button(
    label="Baixar Relatório Completo de Vendas",
    data=df.to_csv(index=False),
    file_name="relatorio_completo_vendas.csv",
    mime="text/csv"
)
