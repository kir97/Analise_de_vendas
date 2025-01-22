import pytest
import sqlite3
import pandas as pd
from scripts.analise_vendas import calcular_faturamento, produto_mais_vendido, calcular_vendas_mensais

@pytest.fixture
def setup_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE registro_vendas (
        id INTEGER PRIMARY KEY,
        produto TEXT,
        quantidade_vendida INTEGER,
        preco_unitario REAL,
        data_venda TEXT
    )
    ''')
    cursor.executemany('''
    INSERT INTO registro_vendas (produto, quantidade_vendida, preco_unitario, data_venda)
    VALUES (?, ?, ?, ?)
    ''', [
        ('Produto A', 10, 100.0, '2024-01-01'),
        ('Produto B', 5, 200.0, '2024-01-01'),
        ('Produto A', 7, 100.0, '2024-01-02'),
        ('Produto B', 3, 200.0, '2024-01-02'),
    ])
    conn.commit()
    return conn

def test_calcular_faturamento(setup_db):
    conn = setup_db
    df = pd.read_sql_query("SELECT * FROM registro_vendas;", conn)
    faturamento_total = calcular_faturamento(df)
    assert faturamento_total == 1700.0

def test_produto_mais_vendido(setup_db):
    conn = setup_db
    df = pd.read_sql_query("SELECT * FROM registro_vendas;", conn)
    produto, quantidade = produto_mais_vendido(df)
    assert produto == 'Produto A'
    assert quantidade == 17

def test_calcular_vendas_mensais(setup_db):
    conn = setup_db
    df = pd.read_sql_query("SELECT * FROM registro_vendas;", conn)
    vendas_mensais = calcular_vendas_mensais(df)
    assert vendas_mensais['2024-01'].sum() == 1700.0