import unittest
import sqlite3
import pandas as pd
import sys
import os

# Adiciona o diretório 'scripts' ao caminho de importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from analise_vendas import carregar_dados_do_banco, calcular_faturamento, produto_mais_vendido, calcular_vendas_mensais

class TestAnaliseVendas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Cria o banco de dados em memória
        cls.conn = sqlite3.connect(":memory:")
        cursor = cls.conn.cursor()
        
        # Criação da tabela no banco de dados em memória
        cursor.execute(''' 
        CREATE TABLE registro_vendas (
            "ID da Venda" INTEGER PRIMARY KEY,
            "Data da Venda" TEXT,
            Produto TEXT,
            "Quantidade Vendida" INTEGER,
            "Preço Unitário" REAL,
            "Custo Unitário" REAL,
            "Desconto Aplicado" REAL,
            Categoria TEXT,
            Regiao TEXT,
            "Data de Entrega" TEXT,
            Vendedor TEXT,
            "Status de Pagamento" TEXT,
            "Método de Pagamento" TEXT
        )
        ''')
        
        # Insere dados de exemplo na tabela
        cursor.executemany(''' 
        INSERT INTO registro_vendas ("Data da Venda", Produto, "Quantidade Vendida", "Preço Unitário", "Custo Unitário", "Desconto Aplicado", Categoria, Regiao, "Data de Entrega", Vendedor, "Status de Pagamento", "Método de Pagamento")
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [
            ('2025-01-01', 'Camiseta Esportiva', 10, 50, 30, 5, 'Esporte', 'Norte', '2025-01-03', 'João', 'Pago', 'Cartão de Crédito'),
            ('2025-01-02', 'Tênis Corrida', 5, 300, 180, 10, 'Esporte', 'Sul', '2025-01-05', 'Maria', 'Pendente', 'Boleto Bancário'),
            ('2025-01-03', 'Mochila Viagem', 3, 150, 90, 0, 'Viagem', 'Sudeste', '2025-01-07', 'Pedro', 'Pago', 'Cartão de Crédito'),
            ('2025-01-04', 'Tênis Corrida', 8, 300, 180, 15, 'Esporte', 'Norte', '2025-01-07', 'João', 'Pago', 'Cartão de Crédito'),
            ('2025-02-01', 'Camiseta Esportiva', 15, 50, 30, 10, 'Esporte', 'Nordeste', '2025-02-03', 'Maria', 'Pendente', 'Boleto Bancário'),
            ('2025-02-02', 'Mochila Viagem', 7, 150, 90, 5, 'Viagem', 'Sul', '2025-02-05', 'Pedro', 'Pago', 'Cartão de Crédito'),
            ('2025-02-03', 'Tênis Corrida', 6, 300, 180, 20, 'Esporte', 'Sudeste', '2025-02-06', 'João', 'Pago', 'Cartão de Crédito'),
            ('2025-02-04', 'Camiseta Casual', 12, 40, 25, 0, 'Casual', 'Norte', '2025-02-06', 'Maria', 'Pago', 'Cartão de Crédito'),
        ])
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        # Fecha a conexão com o banco de dados
        cls.conn.close()

    def test_calcular_faturamento(self):
        df = pd.read_sql_query("SELECT * FROM registro_vendas;", self.conn)
        faturamento_total = calcular_faturamento(df)
        faturamento_esperado = (10 * 50 - 5) + (5 * 300 - 10) + (3 * 150 - 0) + (8 * 300 - 15)
        self.assertEqual(faturamento_total, faturamento_esperado)

    def test_produto_mais_vendido(self):
        df = pd.read_sql_query("SELECT * FROM registro_vendas;", self.conn)
        produto, quantidade = produto_mais_vendido(df)
        self.assertEqual(produto, 'Tênis Corrida')
        self.assertEqual(quantidade, 14)

    def test_calcular_vendas_mensais(self):
        df = pd.read_sql_query("SELECT * FROM registro_vendas;", self.conn)
        vendas_mensais = calcular_vendas_mensais(df)

        # Convertendo o índice para string para garantir que '2025-01' esteja no formato correto
        vendas_mensais.index = vendas_mensais.index.astype(str)

        # Verifique se o mês de janeiro de 2025 está presente no índice
        self.assertTrue('2025-01' in vendas_mensais.index, "Mês de janeiro de 2025 não encontrado")

        # Calcule o faturamento esperado para janeiro de 2025
        faturamento_esperado_janeiro = (10 * 50 - 5) + (5 * 300 - 10) + (3 * 150 - 0) + (8 * 300 - 15)
        self.assertEqual(vendas_mensais['2025-01'], faturamento_esperado_janeiro)

if __name__ == '__main__':
    unittest.main()
