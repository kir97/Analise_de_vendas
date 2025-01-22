import pandas as pd
import sqlite3

def carregar_dados_do_banco():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect("./data/dataset_vendas_ficticias.db")  # Ajuste o caminho conforme necessário
    df = pd.read_sql_query("SELECT * FROM registro_vendas;", conn)
    return df

def calcular_faturamento(df):
    # Calcular o faturamento total, considerando o desconto aplicado
    df["Faturamento"] = (df["Quantidade Vendida"] * df["Preço Unitário"]) - df["Desconto Aplicado"]
    faturamento_total = df["Faturamento"].sum()
    return faturamento_total

def produto_mais_vendido(df):
    # Identificar o produto mais vendido
    produto_quantidade = df.groupby("Produto")["Quantidade Vendida"].sum()
    produto_mais_vendido = produto_quantidade.idxmax()
    quantidade_mais_vendida = produto_quantidade.max()
    return produto_mais_vendido, quantidade_mais_vendida

def calcular_vendas_mensais(df):
    # Calcular as vendas mensais
    df["Data da Venda"] = pd.to_datetime(df["Data da Venda"])  # Remover o 'unit=s'
    df["Mês"] = df["Data da Venda"].dt.to_period("M")  # Convertendo para período mensal
    df["Faturamento"] = (df["Quantidade Vendida"] * df["Preço Unitário"]) - df["Desconto Aplicado"]
    
    # Agrupando e somando o faturamento por mês
    vendas_mensais = df.groupby("Mês")["Faturamento"].sum()

    return vendas_mensais

# Função principal para execução do script
def main():
    # Carregar dados
    df = carregar_dados_do_banco()

    # Calcular o faturamento total
    faturamento_total = calcular_faturamento(df)
    print(f"Faturamento Total: R$ {faturamento_total:,.2f}")

    # Identificar o produto mais vendido
    produto, quantidade = produto_mais_vendido(df)
    print(f"Produto Mais Vendido: {produto} ({quantidade} unidades)")

    # Calcular as vendas mensais
    vendas_mensais = calcular_vendas_mensais(df)
    print("\nFaturamento Mensal:")
    print(vendas_mensais)

    # Exportar o relatório para um arquivo CSV
    relatorio_mensal = vendas_mensais.reset_index()
    relatorio_mensal.columns = ["Mês", "Faturamento"]
    relatorio_mensal.to_csv("relatorio_faturamento_mensal.csv", index=False)
    print("\nRelatório exportado para 'relatorio_faturamento_mensal.csv'")

# Chama a função principal
if __name__ == "__main__":
    main()
