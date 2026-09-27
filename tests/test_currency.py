"""
Pruebas unitarias para el módulo de conversión y formateo de moneda colombiana.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

import unittest
from core.currency import (
    numero_a_letras, formato_moneda_letras,
    formato_moneda_colombiana, parsear_valor_moneda
)


class TestCurrency(unittest.TestCase):

    def test_numero_a_letras_basico(self):
        self.assertEqual(numero_a_letras(0), "CERO")
        self.assertEqual(numero_a_letras(1), "UN")
        self.assertEqual(numero_a_letras(15), "QUINCE")
        self.assertEqual(numero_a_letras(20), "VEINTE")
        self.assertEqual(numero_a_letras(25), "VEINTICINCO")
        self.assertEqual(numero_a_letras(100), "CIEN")
        self.assertEqual(numero_a_letras(105), "CIENTO CINCO")

    def test_numero_a_letras_miles_y_millones(self):
        self.assertEqual(numero_a_letras(1000), "MIL")
        self.assertEqual(numero_a_letras(2000), "DOS MIL")
        self.assertEqual(numero_a_letras(1500000), "UN MILLÓN QUINIENTOS MIL")
        self.assertEqual(numero_a_letras(2000000), "DOS MILLONES")

    def test_formato_moneda_letras(self):
        self.assertEqual(formato_moneda_letras(1), "UN PESO M/CTE.")
        self.assertEqual(formato_moneda_letras(1000000), "UN MILLÓN DE PESOS M/CTE.")
        self.assertEqual(formato_moneda_letras(800000), "OCHOCIENTOS MIL PESOS M/CTE.")
        self.assertEqual(formato_moneda_letras(1500000), "UN MILLÓN QUINIENTOS MIL PESOS M/CTE.")

    def test_formato_moneda_colombiana(self):
        self.assertEqual(formato_moneda_colombiana(800000, con_decimales=False), "$800.000")
        self.assertEqual(formato_moneda_colombiana(1500000, con_decimales=True), "$1.500.000,00")
        self.assertEqual(formato_moneda_colombiana(1500000, con_decimales=False, con_cop=True), "$1.500.000 COP")

    def test_parsear_valor_moneda(self):
        self.assertEqual(parsear_valor_moneda("$1.500.000,00"), 1500000.0)
        self.assertEqual(parsear_valor_moneda("$800.000 COP"), 800000.0)
        self.assertEqual(parsear_valor_moneda("  150000  "), 150000.0)
        self.assertEqual(parsear_valor_moneda(""), 0.0)


if __name__ == "__main__":
    unittest.main()
