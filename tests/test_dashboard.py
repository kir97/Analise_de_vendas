import unittest
import pandas as pd

from scripts.dashboard import (
    df,  # DataFrame carregado no script
)

class TestDashboard(unittest.TestCase):

    def setUp(self):
        # Dados fictícios para testes
        data = {
            "Produto": ["Produto A", "Produto B", "Produto A", "Produto C"],
            "Quantidade Vendida": [10, 5, 15, 8],
            "Preço Unitário": [20.0, 30.0, 20.0, 50.0],
            "Custo Unitário": [10.0, 15.0, 10.0, 20.0],
            "Desconto Aplicado": [10.0, 5.0, 20.0, 10.0],
            "Data da Venda": ["2025-01-01", "2025-01-02", "2025-01-15", "2025-02-01"],
            "Categoria": ["Eletrônicos", "Eletrônicos", "Moda", "Casa"],
            "Região": ["Sul", "Norte", "Sul", "Norte"],
            "Vendedor": ["João", "Maria", "João", "Pedro"],
            "Método de Pagamento": ["Cartão", "Boleto", "Cartão", "Pix"],
            "Status de Pagamento": ["Pago", "Pendente", "Pago", "Pago"],
        }
        self.df = pd.DataFrame(data)

    def test_calcular_faturamento_total(self):
        self.df["Faturamento"] = self.df["Quantidade Vendida"] * self.df["Preço Unitário"]
        faturamento_total = self.df["Faturamento"].sum()
        self.assertAlmostEqual(faturamento_total, 1300.0, places=2)

    def test_calcular_margem_lucro(self):
        self.df["Margem de Lucro"] = (self.df["Preço Unitário"] - self.df["Custo Unitário"]) * self.df["Quantidade Vendida"]
        margem_lucro_total = self.df["Margem de Lucro"].sum()
        self.assertAlmostEqual(margem_lucro_total, 550.0, places=2)

    def test_agrupamento_vendas_mensais(self):
        self.df["Data da Venda"] = pd.to_datetime(self.df["Data da Venda"])
        self.df["Mês"] = self.df["Data da Venda"].dt.to_period("M")
        vendas_mensais = self.df.groupby("Mês")["Faturamento"].sum()

        # Valores esperados
        self.assertAlmostEqual(vendas_mensais["2025-01"], 715.0, places=2)
        self.assertAlmostEqual(vendas_mensais["2025-02"], 490.0, places=2)

    def test_filtro_categoria(self):
        categoria = "Eletrônicos"
        df_filtrado = self.df[self.df["Categoria"] == categoria]
        self.assertEqual(len(df_filtrado), 2)
        self.assertTrue((df_filtrado["Categoria"] == "Eletrônicos").all())

    def test_filtro_produto(self):
        produto = "Produto A"
        df_filtrado = self.df[self.df["Produto"] == produto]
        self.assertEqual(len(df_filtrado), 2)
        self.assertTrue((df_filtrado["Produto"] == "Produto A").all())

if __name__ == "__main__":
    unittest.main()
