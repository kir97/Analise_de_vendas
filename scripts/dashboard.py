import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sqlite3

# Conexão com o banco de dados SQLite (alteração do caminho)
conect = sqlite3.connect("./data/dataset_vendas_ficticias.db")

# Carregar os dados
df = pd.read_sql_query("SELECT * FROM registro_vendas;", conect)

# Calcular o faturamento e a margem de lucro
df["Faturamento"] = df["Quantidade Vendida"] * df["Preço Unitário"]
df["Margem de Lucro"] = (df["Preço Unitário"] - df["Custo Unitário"]) * df["Quantidade Vendida"]

# Calcular as vendas por mês
df["Data da Venda"] = pd.to_datetime(df["Data da Venda"])
df["Mês"] = df["Data da Venda"].dt.to_period("M")
vendas_mensais = df.groupby("Mês")["Faturamento"].sum()

# Calcular as vendas por categoria
vendas_categoria = df.groupby("Categoria")["Faturamento"].sum()

# Calcular as vendas por região
vendas_regiao = df.groupby("Região")["Faturamento"].sum()

# Calcular o desempenho por vendedor
vendas_vendedor = df.groupby("Vendedor")["Faturamento"].sum()

# Calcular as vendas por produto
vendas_produto = df.groupby("Produto")["Faturamento"].sum()

# Calcular descontos aplicados
descontos_aplicados = df["Desconto Aplicado"].sum()

# Calcular status de pagamento
vendas_pagamento = df.groupby("Status de Pagamento")["Faturamento"].sum()

# Calcular vendas por método de pagamento
vendas_metodo_pagamento = df.groupby("Método de Pagamento")["Faturamento"].sum()

# Título do Dashboard
st.title("Dashboard Vendas: Análise Completa")

# Filtros de visualização com opção "Todos"
st.sidebar.header("Filtros")
produto_selecionado = st.sidebar.selectbox("Selecione o Produto", ['Todos'] + list(df["Produto"].unique()))
categoria_selecionada = st.sidebar.selectbox("Selecione a Categoria", ['Todos'] + list(df["Categoria"].unique()))
regiao_selecionada = st.sidebar.selectbox("Selecione a Região", ['Todos'] + list(df["Região"].unique()))
vendedor_selecionado = st.sidebar.selectbox("Selecione o Vendedor", ['Todos'] + list(df["Vendedor"].unique()))
metodo_pagamento_selecionado = st.sidebar.selectbox("Selecione o Método de Pagamento", ['Todos'] + list(df["Método de Pagamento"].unique()))

# Filtrar dados com base nos filtros selecionados
df_filtrado = df[
    ((df["Produto"] == produto_selecionado) | (produto_selecionado == 'Todos')) &
    ((df["Categoria"] == categoria_selecionada) | (categoria_selecionada == 'Todos')) &
    ((df["Região"] == regiao_selecionada) | (regiao_selecionada == 'Todos')) &
    ((df["Vendedor"] == vendedor_selecionado) | (vendedor_selecionado == 'Todos')) &
    ((df["Método de Pagamento"] == metodo_pagamento_selecionado) | (metodo_pagamento_selecionado == 'Todos'))
]

# Exibir KPIs
st.header("KPIs Importantes")
faturamento_total = df_filtrado['Faturamento'].sum()
margem_lucro_total = df_filtrado['Margem de Lucro'].sum()

st.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
st.metric("Margem de Lucro Total", f"R$ {margem_lucro_total:,.2f}")
st.metric("Descontos Aplicados", f"R$ {descontos_aplicados:,.2f}")

# Exibir KPIs de Método de Pagamento interativamente
if metodo_pagamento_selecionado != 'Todos':
    st.header(f"KPIs por {metodo_pagamento_selecionado}")
    vendas_metodo_filtrado = vendas_metodo_pagamento[metodo_pagamento_selecionado]
    st.metric(f"Faturamento por {metodo_pagamento_selecionado}", f"R$ {vendas_metodo_filtrado:,.2f}")

# Gráfico de Faturamento Mensal
st.header("Faturamento Mensal")
vendas_mensais_df = vendas_mensais.reset_index()
vendas_mensais_df["Mês"] = vendas_mensais_df["Mês"].astype(str)  # Convertendo para string

plt.figure(figsize=(10, 6))
sns.lineplot(data=vendas_mensais_df, x="Mês", y="Faturamento", marker='o', color='teal')
plt.title('Faturamento Mensal', fontsize=16)
plt.xlabel('Mês', fontsize=12)
plt.ylabel('Faturamento (R$)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# Gráfico de Vendas por Categoria
st.header("Vendas por Categoria")
vendas_categoria_df = vendas_categoria.reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=vendas_categoria_df, x="Categoria", y="Faturamento", palette='muted')
plt.title('Vendas por Categoria', fontsize=16)
plt.xlabel('Categoria', fontsize=12)
plt.ylabel('Faturamento (R$)', fontsize=12)
plt.tight_layout()
st.pyplot(plt)

# Gráfico de Vendas por Região
st.header("Vendas por Região")
vendas_regiao_df = vendas_regiao.reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=vendas_regiao_df, x="Região", y="Faturamento", palette='Blues')
plt.title('Vendas por Região', fontsize=16)
plt.xlabel('Região', fontsize=12)
plt.ylabel('Faturamento (R$)', fontsize=12)
plt.tight_layout()
st.pyplot(plt)

# Gráfico de Vendas por Vendedor
st.header("Vendas por Vendedor")
vendas_vendedor_df = vendas_vendedor.reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=vendas_vendedor_df, x="Vendedor", y="Faturamento", palette='coolwarm')
plt.title('Vendas por Vendedor', fontsize=16)
plt.xlabel('Vendedor', fontsize=12)
plt.ylabel('Faturamento (R$)', fontsize=12)
plt.tight_layout()
st.pyplot(plt)

# Gráfico de Status de Pagamento
st.header("Status de Pagamento")
vendas_pagamento_df = vendas_pagamento.reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=vendas_pagamento_df, x="Status de Pagamento", y="Faturamento", palette='muted')
plt.title('Status de Pagamento', fontsize=16)
plt.xlabel('Status de Pagamento', fontsize=12)
plt.ylabel('Faturamento (R$)', fontsize=12)
plt.tight_layout()
st.pyplot(plt)

# Análise de Tendência de Vendas
st.header("Análise de Tendência de Vendas")
tendencia_vendas = df.groupby("Data da Venda")[["Faturamento"]].sum().reset_index()

# Corrigir a conversão para números inteiros das datas
tendencia_vendas["Data da Venda"] = pd.to_datetime(tendencia_vendas["Data da Venda"]).astype(int) / 10**9  # Convertendo para timestamp numérico

plt.figure(figsize=(10, 6))
sns.regplot(data=tendencia_vendas, x="Data da Venda", y="Faturamento", scatter_kws={'s': 10}, line_kws={'color': 'red'})
plt.title('Tendência de Vendas ao Longo do Tempo', fontsize=16)
plt.xlabel('Data da Venda', fontsize=12)
plt.ylabel('Faturamento (R$)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# Exportar relatório como CSV (caso o usuário queira baixar)
st.download_button(
    label="Baixar Relatório Completo de Vendas",
    data=df.to_csv(index=False),
    file_name="relatorio_completo_vendas.csv",
    mime="text/csv"
)

# Mostrar dados filtrados
st.sidebar.header("Dados Filtrados")
st.sidebar.write(df_filtrado)
