import unittest
import pandas as pd
from scripts.analise_vendas import (
    carregar_dados_do_banco,
    calcular_faturamento,
    produto_mais_vendido,
    calcular_vendas_mensais,
)

class TestAnaliseVendas(unittest.TestCase):

    def setUp(self):
        # Dados fictícios para os testes
        data = {
            "Produto": ["Produto A", "Produto B", "Produto A", "Produto C"],
            "Quantidade Vendida": [10, 5, 15, 8],
            "Preço Unitário": [20.0, 30.0, 20.0, 50.0],
            "Desconto Aplicado": [10.0, 5.0, 20.0, 10.0],
            "Custo Unitário": [15.0, 25.0, 18.0, 40.0],  # Adicionando custo unitário
            "Data da Venda": ["2025-01-01", "2025-01-02", "2025-01-15", "2025-02-01"],
        }
        self.df = pd.DataFrame(data)
        self.df["Margem de Lucro"] = (self.df["Preço Unitário"] - self.df["Custo Unitário"]) * self.df["Quantidade Vendida"]

    def test_calcular_faturamento(self):
        # Teste do cálculo de faturamento
        faturamento_total = calcular_faturamento(self.df)
        self.assertAlmostEqual(faturamento_total, 1205.0, places=2)

    def test_produto_mais_vendido(self):
        # Teste do produto mais vendido
        produto, quantidade = produto_mais_vendido(self.df)
        self.assertEqual(produto, "Produto A")
        self.assertEqual(quantidade, 25)

    def test_calcular_vendas_mensais(self):
        # Teste do cálculo de vendas mensais
        vendas_mensais = calcular_vendas_mensais(self.df)
        faturamento_jan = vendas_mensais["2025-01"]
        faturamento_fev = vendas_mensais["2025-02"]

        self.assertAlmostEqual(faturamento_jan, 715.0, places=2)
        self.assertAlmostEqual(faturamento_fev, 490.0, places=2)

    def test_margem_lucro(self):
        # Teste de cálculo de margem de lucro
        margem_lucro_total = self.df["Margem de Lucro"].sum()
        self.assertAlmostEqual(margem_lucro_total, 235.0, places=2)  # Valor esperado baseado nos dados fictícios

if __name__ == "__main__":
    unittest.main()
