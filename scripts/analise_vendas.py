import pandas as pd

# Carregar o dataset
file_path = "dataset_vendas_ficticias.csv"
df = pd.read_csv(file_path)

# Calcular o faturamento total
df["Faturamento"] = df["Quantidade Vendida"] * df["Preço Unitário"]
faturamento_total = df["Faturamento"].sum()

# Identificar o produto mais vendido
produto_mais_vendido = df.groupby("Produto")["Quantidade Vendida"].sum().idxmax()
quantidade_mais_vendida = df.groupby("Produto")["Quantidade Vendida"].sum().max()

# Calcular as vendas por período (mensal)
df["Data da Venda"] = pd.to_datetime(df["Data da Venda"])
df["Mês"] = df["Data da Venda"].dt.to_period("M")
vendas_mensais = df.groupby("Mês")["Faturamento"].sum()

# Exibir resultados
print("=== Relatório de Vendas ===")
print(f"Faturamento Total: R$ {faturamento_total:,.2f}")
print(f"Produto Mais Vendido: {produto_mais_vendido} ({quantidade_mais_vendida} unidades)")
print("\nFaturamento Mensal:")
print(vendas_mensais)

# Exportar o relatório para um arquivo CSV
relatorio_mensal = vendas_mensais.reset_index()
relatorio_mensal.columns = ["Mês", "Faturamento"]
relatorio_mensal.to_csv("relatorio_faturamento_mensal.csv", index=False)
print("\nRelatório exportado para 'relatorio_faturamento_mensal.csv'")
