import pandas as pd
import sqlite3

def carregar_dados_do_banco():
    # Conectar ao banco de dados SQLite
    try:
        conn = sqlite3.connect("./data/dataset_vendas_ficticias.db")  # Ajuste o caminho conforme necessário
        df = pd.read_sql_query("SELECT * FROM registro_vendas;", conn)
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    finally:
        conn.close()  # Fechar a conexão após o uso
    return df

def calcular_faturamento(df):
    # Calcular o faturamento total, considerando o desconto aplicado
    df["Faturamento"] = (df["Quantidade Vendida"] * df["Preço Unitário"]) - df["Desconto Aplicado"]
    return df["Faturamento"].sum()

def produto_mais_vendido(df):
    # Identificar o produto mais vendido
    produto_quantidade = df.groupby("Produto")["Quantidade Vendida"].sum()
    return produto_quantidade.idxmax(), produto_quantidade.max()

def calcular_vendas_mensais(df):
    # Calcular as vendas mensais
    df["Data da Venda"] = pd.to_datetime(df["Data da Venda"])  
    df["Mês"] = df["Data da Venda"].dt.to_period("M")  # Convertendo para período mensal
    return df.groupby("Mês")["Faturamento"].sum()

def main():
    # Carregar dados
    df = carregar_dados_do_banco()
    if df is None:
        return  # Se não conseguir carregar os dados, interrompe a execução

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
