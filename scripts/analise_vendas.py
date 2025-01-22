import pandas as pd
import sqlite3

# Conexão com o banco de dados SQLite
conect = sqlite3.connect("./data/dataset_vendas_ficticias.db")

# Carregar os dados da tabela "registro_vendas"
df = pd.read_sql_query("SELECT * FROM registro_vendas;", conect)

# Calcular o faturamento total
df["Faturamento"] = df["Quantidade Vendida"] * df["Preço Unitário"]
faturamento_total = df["Faturamento"].sum()

# Identificar o produto mais vendido
produto_mais_vendido = df.groupby("Produto")["Quantidade Vendida"].sum().
