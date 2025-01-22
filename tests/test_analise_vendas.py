import pytest
import sqlite3
import pandas as pd
import sys
import os

# Adicionando o diretório scripts ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from analise_vendas import calcular_faturamento, produto_mais_vendido, calcular_vendas_mensais

@pytest.fixture
def setup_db():
    conn = sqlite3.connect(":memory:")  # Usando um banco em memória para os testes
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE registro_vendas (
        "ID da Venda" INTEGER PRIMARY KEY,
        "Data da Venda" NUM,
        Produto TEXT,
        "Quantidade Vendida" INTEGER,
        "Preço Unitário" REAL,
        "Custo Unitário" REAL,
        "Desconto Aplicado" REAL,
        Categoria TEXT,
        Regiao TEXT,
        "Data de Entrega" NUM,
        Vendedor TEXT,
        "Status de Pagamento" TEXT,
        "Método de Pagamento" TEXT
    )
    ''')
    cursor.executemany('''
    INSERT INTO registro_vendas ("Data da Venda", Produto, "Quantidade Vendida", "Preço Unitário", "Custo Unitário", "Desconto Aplicado", Categoria, Regiao, "Data de Entrega", Vendedor, "Status de Pagamento", "Método de Pagamento")
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [
        (1682966400, 'Produto A', 10, 100.0, 60.0, 10.0, 'Categoria 1', 'Norte', 1683072000, 'Vendedor 1', 'Pago', 'Cartão'),
        (1682966400, 'Produto B', 5, 200.0, 120.0, 20.0, 'Categoria 2', 'Sul', 1683072000, 'Vendedor 2', 'Pendente', 'Boleto'),
        (1683052800, 'Produto A', 7, 100.0, 60.0, 5.0, 'Categoria 1', 'Centro-Oeste', 1683158400, 'Vendedor 1', 'Pago', 'Cartão'),
        (1683052800, 'Produto B', 3, 200.0, 120.0, 10.0, 'Categoria 2', 'Nordeste', 1683158400, 'Vendedor 2', 'Pendente', 'Boleto'),
    ])
    conn.commit()
    return conn

def test_calcular_faturamento(setup_db):
    conn = setup_db
    df = pd.read_sql_query("SELECT * FROM registro_vendas;", conn)
    faturamento_total = calcular_faturamento(df)
    # O faturamento total é calculado levando em consideração o desconto aplicado
    faturamento_esperado = (10 * 100.0 - 10.0) + (5 * 200.0 - 20.0) + (7 * 100.0 - 5.0) + (3 * 200.0 - 10.0)
    assert faturamento_total == faturamento_esperado

def test_produto_mais_vendido(setup_db):
    conn = setup_db
    df = pd.read_sql_query("SELECT * FROM registro_vendas;", conn)
    produto, quantidade = produto_mais_vendido(df)
    # Produto A é o mais vendido com 17 unidades
    assert produto == 'Produto A'
    assert quantidade == 17

def test_calcular_vendas_mensais(setup_db):
    conn = setup_db
    df = pd.read_sql_query("SELECT * FROM registro_vendas;", conn)
    vendas_mensais = calcular_vendas_mensais(df)
    # O faturamento mensal para janeiro de 2024
    faturamento_esperado_janeiro = (10 * 100.0 - 10.0) + (5 * 200.0 - 20.0) + (7 * 100.0 - 5.0) + (3 * 200.0 - 10.0)
    # A data foi inserida como timestamps, por isso ajusta a comparação para "2024-01"
    assert vendas_mensais['2024-01'].sum() == faturamento_esperado_janeiro
