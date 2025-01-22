# utils.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Função para calcular o faturamento de uma venda
def calcular_faturamento(quantidade_vendida, preco_unitario):
    return quantidade_vendida * preco_unitario

# Função para calcular a média de vendas por produto
def media_vendas_por_produto(df, produto):
    vendas_produto = df[df['Produto'] == produto]
    return vendas_produto['Quantidade Vendida'].mean()

# Função para calcular o total de vendas de um produto
def total_vendas_produto(df, produto):
    vendas_produto = df[df['Produto'] == produto]
    return vendas_produto['Quantidade Vendida'].sum()

# Função para carregar e limpar dados de um CSV
def carregar_dados(caminho):
    df = pd.read_csv(caminho)
    df.dropna(inplace=True)  # Remover linhas com dados faltantes
    return df

# Função para formatar valores monetários
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}"

# Função para converter datas no formato adequado
def converter_data(df, coluna_data):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    return df

# Função para validar se um valor é um número positivo
def validar_numero_positivo(valor):
    if valor < 0:
        raise ValueError("O valor deve ser positivo.")
    return valor

# Função para gerar gráfico de linha de faturamento mensal
def grafico_faturamento_mensal(df):
    df['Mês'] = df['Data da Venda'].dt.to_period('M')
    vendas_mensais = df.groupby('Mês')['Faturamento'].sum()
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=vendas_mensais, marker='o', color='blue')
    plt.title('Faturamento Mensal', fontsize=16)
    plt.xlabel('Mês', fontsize=12)
    plt.ylabel('Faturamento (R$)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt