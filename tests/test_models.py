"""
Pruebas unitarias para modelos, plantillas y exportación a Excel.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

import os
import unittest
import tempfile
from core.models import ItemCotizacion, DatosCotizacion, DatosCuentaCobro
from templates.cotizacion_template import render_cotizacion_html
from templates.cuenta_cobro_template import render_cuenta_cobro_html
from services.excel_service import exportar_cotizacion_excel


class TestModelsAndTemplates(unittest.TestCase):

    def setUp(self):
        self.item1 = ItemCotizacion(descripcion="Mantenimiento preventivo", cantidad=5, precio_unitario=60000.0)
        self.item2 = ItemCotizacion(descripcion="Switch Gigabit TP-Link", cantidad=1, precio_unitario=150000.0)

    def test_item_calculo_total(self):
        self.assertEqual(self.item1.total, 300000.0)
        self.assertEqual(self.item2.total, 150000.0)

    def test_datos_cotizacion_totales(self):
        datos = DatosCotizacion(
            cliente="Colegio Técnico",
            emisor="Owen Badel Hooker",
            rut_emisor="1.047.503.800",
            fecha="27 de septiembre de 2026",
            items=[self.item1, self.item2]
        )
        self.assertEqual(datos.total_general, 450000.0)
        self.assertEqual(datos.total_en_letras, "CUATROCIENTOS CINCUENTA MIL PESOS M/CTE.")

    def test_render_cotizacion_html(self):
        datos = DatosCotizacion(
            cliente="Empresa XYZ",
            emisor="Owen Badel Hooker",
            rut_emisor="1.047.503.800",
            fecha="27 de septiembre de 2026",
            objetivo_servicio="Optimización de infraestructura de redes",
            items=[self.item1]
        )
        html_out = render_cotizacion_html(datos)
        self.assertIn("Empresa XYZ", html_out)
        self.assertIn("Owen Badel Hooker", html_out)
        self.assertIn("Mantenimiento preventivo", html_out)
        self.assertIn("$300.000,00", html_out)

    def test_exportar_excel(self):
        datos = DatosCotizacion(
            cliente="Cliente Test",
            emisor="Owen Badel Hooker",
            rut_emisor="1.047.503.800",
            fecha="27 de septiembre de 2026",
            items=[self.item1, self.item2]
        )
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tf:
            temp_path = tf.name

        try:
            exito = exportar_cotizacion_excel(datos, temp_path)
            self.assertTrue(exito)
            self.assertTrue(os.path.exists(temp_path))
            self.assertGreater(os.path.getsize(temp_path), 1000)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
