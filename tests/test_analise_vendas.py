import unittest
import sqlite3
import pandas as pd
from scripts.analise_vendas import calcular_faturamento, produto_mais_vendido, calcular_vendas_mensais

class TestAnaliseVendas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(":memory:")
        cursor = cls.conn.cursor()
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
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_calcular_faturamento(self):
        df = pd.read_sql_query("SELECT * FROM registro_vendas;", self.conn)
        faturamento_total = calcular_faturamento(df)
        faturamento_esperado = (10 * 100.0 - 10.0) + (5 * 200.0 - 20.0) + (7 * 100.0 - 5.0) + (3 * 200.0 - 10.0)
        self.assertEqual(faturamento_total, faturamento_esperado)

    def test_produto_mais_vendido(self):
        df = pd.read_sql_query("SELECT * FROM registro_vendas;", self.conn)
        produto, quantidade = produto_mais_vendido(df)
        self.assertEqual(produto, 'Produto A')
        self.assertEqual(quantidade, 17)

    def test_calcular_vendas_mensais(self):
        df = pd.read_sql_query("SELECT * FROM registro_vendas;", self.conn)
        vendas_mensais = calcular_vendas_mensais(df)
        faturamento_esperado_janeiro = (10 * 100.0 - 10.0) + (5 * 200.0 - 20.0) + (7 * 100.0 - 5.0) + (3 * 200.0 - 10.0)
        self.assertEqual(vendas_mensais['2025-01'].sum(), faturamento_esperado_janeiro)

if __name__ == '__main__':
    unittest.main()
