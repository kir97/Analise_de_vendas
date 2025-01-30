import os
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configuração de caminhos
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
db_path = os.path.join(base_path, "dataset_vendas_ficticias.db")
csv_path = os.path.join(base_path, "dataset_vendas_ficticias.csv")

# Função para carregar dados do banco de dados SQLite
@st.cache_data
def carregar_dados_db(db_path):
    try:
        with sqlite3.connect(db_path) as conect:
            return pd.read_sql_query("SELECT * FROM registro_vendas;", conect)
    except Exception as e:
        st.error(f"Erro ao carregar dados do banco de dados: {e}")
        return None

# Função para carregar dados do CSV
@st.cache_data
def carregar_dados_csv(csv_path):
    try:
        return pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"Erro ao carregar dados do CSV: {e}")
        return None

# Carregar os dados (prioridade: banco -> CSV)
def carregar_dados():
    try:
        if os.path.exists(db_path):
            df = carregar_dados_db(db_path)
            fonte = "Banco de Dados SQLite"
        elif os.path.exists(csv_path):
            df = carregar_dados_csv(csv_path)
            fonte = "Arquivo CSV"
        else:
            st.error("Nenhuma fonte de dados encontrada! Verifique o banco de dados ou o arquivo CSV.")
            st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        st.stop()
    
    st.sidebar.success(f"Dados carregados da fonte: {fonte}")
    return df

# Função para processar e limpar os dados
def processar_dados(df):
    df["Data da Venda"] = pd.to_datetime(df["Data da Venda"])
    df["Faturamento"] = df["Quantidade Vendida"] * df["Preço Unitário"]
    df["Margem de Lucro"] = (df["Preço Unitário"] - df["Custo Unitário"]) * df["Quantidade Vendida"]
    
    # Adicionar novas colunas para análise
    df["Lucro Líquido"] = df["Faturamento"] - (df["Custo Unitário"] * df["Quantidade Vendida"])
    df["Mês"] = df["Data da Venda"].dt.to_period("M")
    df["Ano"] = df["Data da Venda"].dt.year
    df["Categoria"] = df["Categoria"].fillna("Desconhecida")  # Tratar valores ausentes

    return df

# Função para calcular KPIs
def calcular_kpis(df_filtrado):
    faturamento_total = df_filtrado['Faturamento'].sum()
    margem_lucro_total = df_filtrado['Margem de Lucro'].sum()
    lucro_liquido_total = df_filtrado['Lucro Líquido'].sum()
    
    return faturamento_total, margem_lucro_total, lucro_liquido_total

# Função para criar gráfico de faturamento mensal
def grafico_faturamento_mensal(df_filtrado):
    vendas_mensais = df_filtrado.groupby("Mês")["Faturamento"].sum().reset_index()
    vendas_mensais["Mês"] = vendas_mensais["Mês"].astype(str)
    
    fig = px.line(vendas_mensais, x="Mês", y="Faturamento", title='Faturamento Mensal', markers=True)
    fig.update_layout(template="plotly_dark")
    return fig

# Função para criar gráfico de vendas por categoria
def grafico_vendas_categoria(df_filtrado):
    vendas_categoria = df_filtrado.groupby("Categoria")["Faturamento"].sum().reset_index()
    fig = px.bar(vendas_categoria, x="Categoria", y="Faturamento", title="Vendas por Categoria", color="Faturamento", color_continuous_scale="Viridis")
    fig.update_layout(template="plotly_dark")
    return fig

# Função para criar gráfico de distribuição de lucro líquido por produto
def grafico_lucro_produto(df_filtrado):
    lucro_produto = df_filtrado.groupby("Produto")["Lucro Líquido"].sum().reset_index()
    fig = px.bar(lucro_produto, x="Produto", y="Lucro Líquido", title="Lucro Líquido por Produto", color="Lucro Líquido", color_continuous_scale="Plasma")
    fig.update_layout(template="plotly_dark")
    return fig

# Função para exportar relatório como CSV
def exportar_relatorio(df_filtrado):
    return df_filtrado.to_csv(index=False)

# Função principal do Dashboard
def main():
    # Carregar e processar os dados
    df = carregar_dados()
    df = processar_dados(df)
    
    # Filtros de visualização
    st.sidebar.header("Filtros")
    produto_selecionado = st.sidebar.selectbox("Selecione o Produto", ['Todos'] + list(df["Produto"].unique()))
    df_filtrado = df[(df["Produto"] == produto_selecionado) | (produto_selecionado == 'Todos')]

    # Exibir KPIs
    st.header("KPIs Importantes")
    faturamento_total, margem_lucro_total, lucro_liquido_total = calcular_kpis(df_filtrado)
    st.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
    st.metric("Margem de Lucro Total", f"R$ {margem_lucro_total:,.2f}")
    st.metric("Lucro Líquido Total", f"R$ {lucro_liquido_total:,.2f}")

    # Gráficos
    st.header("Visualizações")
    st.subheader("Faturamento Mensal")
    st.plotly_chart(grafico_faturamento_mensal(df_filtrado))
    
    st.subheader("Vendas por Categoria")
    st.plotly_chart(grafico_vendas_categoria(df_filtrado))

    st.subheader("Lucro Líquido por Produto")
    st.plotly_chart(grafico_lucro_produto(df_filtrado))

    # Exportar Relatório
    st.download_button(
        label="Baixar Relatório Completo de Vendas",
        data=exportar_relatorio(df_filtrado),
        file_name="relatorio_completo_vendas.csv",
        mime="text/csv"
    )

    # Adicionar créditos ao final da barra lateral
    st.sidebar.markdown("🚀 Desenvolvido por Lúcio Ferreira e Willian Santana")

# Executa a aplicação
if __name__ == "__main__":
    main()
