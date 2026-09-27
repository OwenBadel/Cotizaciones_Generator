"""
Pruebas unitarias para modelos, plantillas y exportación a Excel.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

import os
import unittest
import tempfile
from core.models import ItemCotizacion, DatosCotizacion, DatosCuentaCobro
from core.catalog import CATALOGO_SERVICIOS_TI
from templates.cotizacion_template import render_cotizacion_html
from templates.cuenta_cobro_template import render_cuenta_cobro_html
from services.excel_service import exportar_cotizacion_excel, exportar_cuenta_cobro_excel


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

    def test_datos_cotizacion_descuento_e_iva(self):
        # Subtotal: 450.000. Descuento 10% = 45.000. Base = 405.000. IVA 19% = 76.950. Total = 481.950
        datos = DatosCotizacion(
            cliente="Empresa ABC",
            emisor="Owen Badel Hooker",
            rut_emisor="1.047.503.800",
            fecha="27 de septiembre de 2026",
            descuento_porcentaje=10.0,
            aplicar_iva=True,
            items=[self.item1, self.item2]
        )
        self.assertEqual(datos.subtotal, 450000.0)
        self.assertEqual(datos.descuento_valor, 45000.0)
        self.assertEqual(datos.base_imponible, 405000.0)
        self.assertEqual(datos.iva_valor, 76950.0)
        self.assertEqual(datos.total_general, 481950.0)

    def test_datos_cuenta_cobro_retenciones(self):
        # Subtotal bruto: 1.000.000. Retefuente 4% = 40.000. ReteICA 0.966% = 9.660. Total neto = 950.340
        item = ItemCotizacion(descripcion="Servicios Profesionales de TI", cantidad=1, precio_unitario=1000000.0)
        datos = DatosCuentaCobro(
            num_cuenta="015",
            num_contrato="12 de 2026",
            periodo_ejecucion="01 al 30 de septiembre de 2026",
            periodo_largo="1 al 30 de septiembre de 2026",
            objeto_contrato="Soporte y administración de servidores",
            concepto_cobro="Cobro mensual por actividades realizadas",
            cliente="Entidad Oficial",
            nit_cliente="900.123.456-7",
            ciudad_cliente="Cartagena",
            emisor="Owen Badel Hooker",
            rut_emisor="1.047.503.800",
            lugar_expedicion="de Cartagena",
            telefono="3016450065",
            email="owenbadel19@gmail.com",
            cargo="Ingeniero de Sistemas",
            banco="Bancolombia",
            tipo_cuenta="Ahorros",
            numero_cuenta="67800017891",
            titular_cuenta="Owen Badel Hooker",
            aplicar_retefuente=True,
            retefuente_porcentaje=4.0,
            aplicar_reteica=True,
            reteica_porcentaje=0.966,
            items=[item]
        )
        self.assertEqual(datos.subtotal_bruto, 1000000.0)
        self.assertEqual(datos.retefuente_valor, 40000.0)
        self.assertEqual(datos.reteica_valor, 9660.0)
        self.assertEqual(datos.total_deducciones, 49660.0)
        self.assertEqual(datos.total_general, 950340.0)

    def test_catalogo_servicios(self):
        self.assertGreaterEqual(len(CATALOGO_SERVICIOS_TI), 5)
        for serv in CATALOGO_SERVICIOS_TI:
            self.assertTrue(len(serv.descripcion) > 0)
            self.assertGreater(serv.precio_sugerido, 0)
            self.assertGreaterEqual(serv.cantidad_defecto, 1)

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

    def test_render_cuenta_cobro_html(self):
        item = ItemCotizacion(descripcion="Consultoría Cloud", cantidad=1, precio_unitario=500000.0)
        datos = DatosCuentaCobro(
            num_cuenta="007",
            num_contrato="05-2026",
            periodo_ejecucion="Septiembre 2026",
            periodo_largo="Septiembre de 2026",
            objeto_contrato="Arquitectura Cloud",
            concepto_cobro="Servicio de despliegue",
            cliente="Cliente Cloud",
            nit_cliente="123456",
            ciudad_cliente="Cartagena",
            emisor="Owen Badel Hooker",
            rut_emisor="1.047.503.800",
            lugar_expedicion="de Cartagena",
            telefono="3016450065",
            email="owenbadel19@gmail.com",
            cargo="Arquitecto Cloud",
            banco="Bancolombia",
            tipo_cuenta="Ahorros",
            numero_cuenta="12345678",
            titular_cuenta="Owen Badel Hooker",
            items=[item]
        )
        html_out = render_cuenta_cobro_html(datos)
        self.assertIn("CUENTA DE COBRO N° 007", html_out)
        self.assertIn("Cliente Cloud", html_out)
        self.assertIn("Consultoría Cloud", html_out)

    def test_exportar_excel_cotizacion(self):
        datos = DatosCotizacion(
            cliente="Cliente Test",
            emisor="Owen Badel Hooker",
            rut_emisor="1.047.503.800",
            fecha="27 de septiembre de 2026",
            descuento_porcentaje=5.0,
            aplicar_iva=True,
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

    def test_exportar_excel_cuenta_cobro(self):
        datos = DatosCuentaCobro(
            num_cuenta="099",
            num_contrato="Contrato 99",
            periodo_ejecucion="Septiembre",
            periodo_largo="Septiembre 2026",
            objeto_contrato="Mantenimiento",
            concepto_cobro="Cobro",
            cliente="Cliente Corp",
            nit_cliente="999-9",
            ciudad_cliente="Cartagena",
            emisor="Owen Badel Hooker",
            rut_emisor="1.047.503.800",
            lugar_expedicion="de Cartagena",
            telefono="3016450065",
            email="owenbadel19@gmail.com",
            cargo="Ingeniero de Sistemas",
            banco="Bancolombia",
            tipo_cuenta="Ahorros",
            numero_cuenta="123456",
            titular_cuenta="Owen Badel Hooker",
            aplicar_retefuente=True,
            items=[self.item1]
        )
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tf:
            temp_path = tf.name

        try:
            exito = exportar_cuenta_cobro_excel(datos, temp_path)
            self.assertTrue(exito)
            self.assertTrue(os.path.exists(temp_path))
            self.assertGreater(os.path.getsize(temp_path), 1000)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
