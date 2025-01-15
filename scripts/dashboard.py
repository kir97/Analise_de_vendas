import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3


# Conexão com o banco de dados SQLite (alteração do caminho)
conect = sqlite3.connect("../data/dataset_vendas_ficticias.db")
cursor = conect.cursor()


# Carregar os dados e processar
df = pd.read_sql_query("SELECT * FROM registro_vendas;", conect)

# Calcular o faturamento
df["Faturamento"] = df["Quantidade Vendida"] * df["Preço Unitário"]
faturamento_total = df["Faturamento"].sum()

# Identificar o produto mais vendido
produto_mais_vendido = df.groupby("Produto")["Quantidade Vendida"].sum().idxmax()
quantidade_mais_vendida = df.groupby("Produto")["Quantidade Vendida"].sum().max()

# Calcular as vendas por mês
df["Data da Venda"] = pd.to_datetime(df["Data da Venda"])
df["Mês"] = df["Data da Venda"].dt.to_period("M")
vendas_mensais = df.groupby("Mês")["Faturamento"].sum()

# Título do Dashboard
st.title("Dashboard de Vendas")

# Exibir KPIs
st.header("KPIs Importantes")
st.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
st.metric("Produto Mais Vendido", f"{produto_mais_vendido} ({quantidade_mais_vendida} unidades)")

# Gráfico de Faturamento Mensal
st.header("Faturamento Mensal")

# Melhorando a visualização do gráfico de faturamento mensal
vendas_mensais_df = vendas_mensais.reset_index()
vendas_mensais_df["Mês"] = vendas_mensais_df["Mês"].astype(str)  # Convertendo para string para exibição correta no gráfico

# Gráfico com seaborn e matplotlib
plt.figure(figsize=(10, 6))
sns.lineplot(data=vendas_mensais_df, x="Mês", y="Faturamento", marker='o', color='blue')

# Ajustar título e rótulos
plt.title('Faturamento Mensal', fontsize=16)
plt.xlabel('Mês', fontsize=12)
plt.ylabel('Faturamento (R$)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

# Exibir o gráfico
st.pyplot(plt)

# Exibir o relatório de vendas mensais
st.header("Relatório de Vendas Mensais")
st.write(vendas_mensais)

# Exportar relatório como CSV (caso o usuário queira baixar)
st.download_button(
    label="Baixar Relatório Mensal",
    data=vendas_mensais_df.to_csv(index=False),
    file_name="relatorio_faturamento_mensal.csv",
    mime="text/csv"
)

# Opção de visualizar dados adicionais
st.sidebar.header("Opções de Filtro")
produto_selecionado = st.sidebar.selectbox("Selecione o Produto", df["Produto"].unique())

# Filtrar dados com base no produto selecionado
df_produto = df[df["Produto"] == produto_selecionado]
vendas_produto = df_produto.groupby("Mês")["Faturamento"].sum()

# Exibir gráfico para o produto selecionado
st.sidebar.subheader(f"Faturamento do Produto: {produto_selecionado}")
st.sidebar.line_chart(vendas_produto)

