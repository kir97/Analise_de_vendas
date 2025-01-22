import unittest
import pandas as pd
from scripts.analise_vendas import calcular_faturamento, produto_mais_vendido, calcular_vendas_mensais
import sqlite3

class TestAnaliseVendas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Conectar ao banco de dados SQLite
        cls.conn = sqlite3.connect("./data/dataset_vendas_ficticias.db")  # Ajuste o caminho conforme necessário
        cls.df = pd.read_sql_query("SELECT * FROM registro_vendas;", cls.conn)

    def test_calcular_faturamento(self):
        faturamento_total = calcular_faturamento(self.df)
        faturamento_esperado = (10 * 50 - 5) + (5 * 300 - 10) + (3 * 150 - 0) + (8 * 300 - 15)
        self.assertEqual(faturamento_total, faturamento_esperado)

    def test_calcular_vendas_mensais(self):
        vendas_mensais = calcular_vendas_mensais(self.df)
        # Esperado será baseado nos dados que você tem no banco de dados
        vendas_esperadas = pd.Series([5000, 4500, 7000], index=pd.to_datetime(['2025-01', '2025-02', '2025-03']).to_period('M'))
        pd.testing.assert_series_equal(vendas_mensais, vendas_esperadas)

    def test_produto_mais_vendido(self):
        produto, quantidade = produto_mais_vendido(self.df)
        self.assertEqual(produto, 'Tênis Corrida')  # Ajuste conforme os dados esperados no banco
        self.assertEqual(quantidade, 100)  # Ajuste conforme a quantidade do produto mais vendido

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

if __name__ == "__main__":
    unittest.main()
