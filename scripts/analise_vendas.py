import os
import pandas as pd
import sqlite3

# Caminho base do projeto
base_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(base_path, "..", "data")
csv_path = os.path.join(data_path, "dataset_vendas_ficticias.csv")
db_path = os.path.join(data_path, "dataset_vendas_ficticias.db")

def carregar_dados_do_banco():
    """
    Função para carregar os dados do banco de dados SQLite.
    """
    if not os.path.isfile(db_path):
        print(f"Erro: Banco de dados não encontrado em: {db_path}")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM registro_vendas;", conn)
        conn.close()  # Fechar a conexão após o uso
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    
    return df

def carregar_dados_do_csv():
    """
    Função para carregar os dados do arquivo CSV.
    """
    if not os.path.isfile(csv_path):
        print(f"Erro: Arquivo CSV não encontrado em: {csv_path}")
        return None
    
    return pd.read_csv(csv_path)

def calcular_faturamento(df):
    """
    Função para calcular o faturamento total, considerando o desconto aplicado.
    """
    df["Faturamento"] = (df["Quantidade Vendida"] * df["Preço Unitário"]) - df["Desconto Aplicado"]
    return df["Faturamento"].sum()

def produto_mais_vendido(df):
    """
    Função para identificar o produto mais vendido.
    """
    produto_quantidade = df.groupby("Produto")["Quantidade Vendida"].sum()
    return produto_quantidade.idxmax(), produto_quantidade.max()

def calcular_vendas_mensais(df):
    """
    Função para calcular o faturamento mensal.
    """
    df["Data da Venda"] = pd.to_datetime(df["Data da Venda"])
    df["Mês"] = df["Data da Venda"].dt.to_period("M")
    return df.groupby("Mês")["Faturamento"].sum()

def exportar_relatorio(vendas_mensais):
    """
    Função para exportar os resultados para um arquivo CSV.
    """
    relatorio_mensal = vendas_mensais.reset_index()
    relatorio_mensal.columns = ["Mês", "Faturamento"]
    relatorio_mensal.to_csv(os.path.join(data_path, "relatorio_faturamento_mensal.csv"), index=False)
    print("\nRelatório exportado para 'relatorio_faturamento_mensal.csv'.")

def main():
    # Tentar carregar os dados do banco de dados
    df = carregar_dados_do_banco()
    
    if df is None:
        print("Tentando carregar dados do CSV...")
        df = carregar_dados_do_csv()
    
    # Se não conseguir carregar os dados, interrompe a execução
    if df is None:
        print("Falha ao carregar os dados. O programa será encerrado.")
        return
    
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
    
    # Exportar o relatório para CSV
    exportar_relatorio(vendas_mensais)

# Chama a função principal
if __name__ == "__main__":
    main()
