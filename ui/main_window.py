"""
Ventana Principal de la Suite: Generador Profesional de Cotizaciones y Cuentas de Cobro.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QFileDialog, QGroupBox, QFormLayout,
    QDoubleSpinBox, QSpinBox, QAbstractItemView, QFrame, QComboBox,
    QTabWidget, QCheckBox
)
from PyQt5.QtCore import Qt, QDate

from core.models import ItemCotizacion, DatosCotizacion, DatosCuentaCobro
from core.currency import (
    formato_moneda_colombiana, parsear_valor_moneda
)
from core.config_manager import cargar_configuracion, guardar_configuracion
from core.utils import sanitizar_nombre_archivo, incrementar_consecutivo
from templates.cotizacion_template import render_cotizacion_html
from templates.cuenta_cobro_template import render_cuenta_cobro_html
from services.pdf_service import PDFRenderService
from services.excel_service import exportar_cotizacion_excel
from .styles import APP_QSS


class GeneradorCotizacionesWindow(QMainWindow):
    """Ventana principal para la gestión y exportación de propuestas y cuentas de cobro."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador Profesional de Cotizaciones y Cuentas de Cobro TI — Owen Badel Hooker")
        self.resize(1080, 920)
        self.setMinimumWidth(880)

        self._actualizando = False
        self._current_doc_type = "Cotización"
        self.config = cargar_configuracion()
        self.pdf_service = PDFRenderService(self)

        self.initUI()
        self.aplicar_estilos()

    def aplicar_estilos(self):
        self.setStyleSheet(APP_QSS)

    def initUI(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(12)

        # 1. Header Banner
        header = QFrame()
        header.setObjectName("appHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(22, 14, 22, 14)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        lbl_title = QLabel("Generador Profesional de Cotizaciones y Cuentas de Cobro TI")
        lbl_title.setObjectName("appTitle")
        lbl_sub = QLabel("Servicios Tecnológicos de Infraestructura y Redes · Owen Badel Hooker — Ingeniero de Sistemas")
        lbl_sub.setObjectName("appSubtitle")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_sub)
        header_layout.addLayout(title_box)
        header_layout.addStretch()
        root.addWidget(header)

        # 2. Tabs
        self.tabs = QTabWidget()
        self._setup_tab_cotizacion()
        self._setup_tab_cuenta_cobro()
        root.addWidget(self.tabs)

        # 3. Items Table
        self._setup_items_table(root)

        # 4. Footer & Action Buttons
        self._setup_footer_actions(root)

    def _setup_tab_cotizacion(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(14)

        # Meta Cliente / Emisor
        group_meta = QGroupBox("Datos del Cliente y Emisor")
        form = QFormLayout(group_meta)
        form.setContentsMargins(10, 10, 10, 6)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(8)

        self.input_cliente = QLineEdit(self.config.get("cliente_defecto", "I.E. Técnica de Pasacaballos"))
        self.input_emisor = QLineEdit(self.config.get("emisor", "Owen Badel Hooker"))
        self.input_rut = QLineEdit(self.config.get("rut", "1.047.503.800"))
        self.input_fecha = QLineEdit(QDate.currentDate().toString("dd 'de' MMMM 'de' yyyy"))

        self.combo_pago = QComboBox()
        self.combo_pago.addItem("50% anticipo y 50% al finalizar")
        self.combo_pago.addItem("Pago contra entrega (100%)")
        self.combo_pago.addItem("No incluir forma de pago")

        form.addRow("Cliente:", self.input_cliente)
        form.addRow("Preparado Por:", self.input_emisor)
        form.addRow("NIT / RUT:", self.input_rut)
        form.addRow("Fecha:", self.input_fecha)
        form.addRow("Forma de Pago:", self.combo_pago)
        layout.addWidget(group_meta, stretch=1)

        # Objetivo y Detalle
        group_obj = QGroupBox("Objetivo y Detalle del Servicio")
        layout_obj = QVBoxLayout(group_obj)
        layout_obj.setContentsMargins(10, 10, 10, 6)
        layout_obj.setSpacing(6)

        lbl_obj = QLabel("Objetivo del Servicio:")
        self.input_objetivo = QLineEdit(
            "Suministro e instalación de equipos de red, mantenimiento preventivo "
            "de infraestructura de cómputo y soporte técnico para impresoras, garantizando "
            "la optimización y estabilidad de la red de la institución."
        )
        self.input_objetivo.setCursorPosition(0)

        lbl_det = QLabel("Detalle de Servicios (Viñetas opcionales):")
        self.input_detalle = QTextEdit()
        self.input_detalle.setPlainText(
            "• Mantenimiento Preventivo de Equipos: Limpieza interna, cambio de pasta térmica y optimización.\n"
            "• Equipos de Red y Configuración: Switch TP-Link Gigabit y puntos de acceso configurados.\n"
            "• Soporte Técnico a Impresoras: Instalación de controladores y calibración."
        )
        self.input_detalle.setMaximumHeight(75)

        layout_obj.addWidget(lbl_obj)
        layout_obj.addWidget(self.input_objetivo)
        layout_obj.addWidget(lbl_det)
        layout_obj.addWidget(self.input_detalle)
        layout.addWidget(group_obj, stretch=1)

        self.tabs.addTab(tab, "📄 Cotización / Propuesta")

    def _setup_tab_cuenta_cobro(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(14)

        # Meta Contrato y Fechas
        group_meta = QGroupBox("Contrato, Fechas y Concepto")
        form = QFormLayout(group_meta)
        form.setContentsMargins(10, 10, 10, 6)
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(7)

        self.input_num_cuenta = QLineEdit(self.config.get("consecutivo_cuenta", "001"))
        self.input_num_contrato = QLineEdit(self.config.get("num_contrato", "15 del 31-08-2026"))
        self.input_periodo = QLineEdit(self.config.get("periodo_ejecucion", "31-08-2026 a 07-09-2026"))
        self.input_periodo_largo = QLineEdit(self.config.get("periodo_largo", "31 de agosto al 07 de septiembre de 2026"))
        self.input_objeto_contrato = QLineEdit(self.config.get("objeto_contrato", "Mantenimiento preventivo de computadores y soporte técnico."))

        self.input_concepto_cobro = QTextEdit()
        self.input_concepto_cobro.setMaximumHeight(70)

        btn_regen = QPushButton("🔄 Regenerar Concepto Estándar")
        btn_regen.setCursor(Qt.PointingHandCursor)
        btn_regen.clicked.connect(self._regenerar_concepto)

        form.addRow("N° Cuenta de Cobro:", self.input_num_cuenta)
        form.addRow("Contrato N° y Fecha:", self.input_num_contrato)
        form.addRow("Período de Ejecución:", self.input_periodo)
        form.addRow("Período en Letras:", self.input_periodo_largo)
        form.addRow("Objeto Contractual:", self.input_objeto_contrato)
        form.addRow("Concepto Detallado:", self.input_concepto_cobro)
        form.addRow("", btn_regen)
        layout.addWidget(group_meta, stretch=1)

        # Datos Bancarios y Tributarios
        group_banco = QGroupBox("Datos del Contratante, Banco y Firma")
        form_banco = QFormLayout(group_banco)
        form_banco.setContentsMargins(10, 10, 10, 6)
        form_banco.setHorizontalSpacing(10)
        form_banco.setVerticalSpacing(7)

        self.input_nit_cliente = QLineEdit(self.config.get("nit_cliente", "800.255.974-5"))
        self.input_ciudad_cliente = QLineEdit(self.config.get("ciudad_cliente", "Cartagena de Indias, D.T. y C."))
        self.input_lugar_cc = QLineEdit(self.config.get("lugar_expedicion", "de Cartagena"))
        self.input_telefono = QLineEdit(self.config.get("telefono", "3016450065"))
        self.input_email = QLineEdit(self.config.get("email", "owenbadel19@gmail.com"))
        self.input_cargo = QLineEdit(self.config.get("cargo", "Contratista de Servicios TI"))

        self.combo_banco = QComboBox()
        self.combo_banco.setEditable(True)
        self.combo_banco.addItems(["Bancolombia", "Nequi", "Daviplata", "Davivienda", "Banco de Bogotá", "BBVA", "Banco Agrario"])
        self.combo_banco.setCurrentText(self.config.get("banco", "Bancolombia"))

        self.combo_tipo_cuenta = QComboBox()
        self.combo_tipo_cuenta.addItems(["Ahorros", "Cuenta Corriente", "Billetera Digital"])
        self.combo_tipo_cuenta.setCurrentText(self.config.get("tipo_cuenta", "Ahorros"))

        self.input_num_cuenta_banco = QLineEdit(self.config.get("numero_cuenta", "67800017891"))
        self.input_titular_cuenta = QLineEdit(self.config.get("titular", self.input_emisor.text()))

        box_checks = QHBoxLayout()
        self.check_tributario = QCheckBox("Decl. No IVA (Art. 437)")
        self.check_tributario.setChecked(self.config.get("incluir_tributario", True))
        self.check_firma = QCheckBox("Incluir Firma Digital")
        self.check_firma.setChecked(self.config.get("incluir_firma", True))
        box_checks.addWidget(self.check_tributario)
        box_checks.addWidget(self.check_firma)

        box_contacto = QHBoxLayout()
        box_contacto.addWidget(self.input_telefono)
        box_contacto.addWidget(self.input_email)

        form_banco.addRow("NIT Contratante:", self.input_nit_cliente)
        form_banco.addRow("Ciudad Contratante:", self.input_ciudad_cliente)
        form_banco.addRow("Lugar C.C.:", self.input_lugar_cc)
        form_banco.addRow("Teléfono | Email:", box_contacto)
        form_banco.addRow("Cargo Contratista:", self.input_cargo)
        form_banco.addRow("Entidad Bancaria:", self.combo_banco)
        form_banco.addRow("Tipo de Cuenta:", self.combo_tipo_cuenta)
        form_banco.addRow("N° Cuenta Bancaria:", self.input_num_cuenta_banco)
        form_banco.addRow("Titular Cuenta:", self.input_titular_cuenta)
        form_banco.addRow("Opciones:", box_checks)
        layout.addWidget(group_banco, stretch=1)

        self.tabs.addTab(tab, "💳 Cuenta de Cobro")

        if not self.input_concepto_cobro.toPlainText().strip():
            self._regenerar_concepto()

        self.input_emisor.textChanged.connect(lambda txt: self.input_titular_cuenta.setText(txt))

    def _setup_items_table(self, root: QVBoxLayout):
        group_items = QGroupBox("Ítems y Conceptos de la Propuesta / Cobro")
        layout = QVBoxLayout(group_items)
        layout.setContentsMargins(10, 8, 10, 10)
        layout.setSpacing(10)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Descripción", "Cantidad", "Valor Unitario ($)", "Valor Total ($)"])
        tbl_header = self.table.horizontalHeader()
        tbl_header.setSectionResizeMode(0, QHeaderView.Stretch)
        for col, ancho in ((1, 90), (2, 150), (3, 150)):
            tbl_header.setSectionResizeMode(col, QHeaderView.Interactive)
            tbl_header.resizeSection(col, ancho)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.itemChanged.connect(self.actualizar_total_ui)
        layout.addWidget(self.table)

        # Fila de adición rápida
        add_row = QHBoxLayout()
        self.item_desc = QLineEdit()
        self.item_desc.setPlaceholderText("Descripción del ítem/servicio prestado...")
        self.item_desc.returnPressed.connect(self.agregar_item)

        self.item_cant = QSpinBox()
        self.item_cant.setRange(1, 1000)
        self.item_cant.setValue(1)
        self.item_cant.setAlignment(Qt.AlignCenter)
        self.item_cant.setFixedWidth(90)

        self.item_precio = QDoubleSpinBox()
        self.item_precio.setRange(0, 100000000)
        self.item_precio.setSingleStep(5000)
        self.item_precio.setPrefix("$ ")
        self.item_precio.setAlignment(Qt.AlignRight)
        self.item_precio.setFixedWidth(150)
        self.item_precio.setValue(150000)
        self.item_precio.lineEdit().returnPressed.connect(self.agregar_item)

        btn_add = QPushButton("➕ Añadir")
        btn_add.setObjectName("btnAdd")
        btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.clicked.connect(self.agregar_item)

        btn_del = QPushButton("🗑️ Eliminar")
        btn_del.setObjectName("btnDelete")
        btn_del.setCursor(Qt.PointingHandCursor)
        btn_del.clicked.connect(self.eliminar_item)

        add_row.addWidget(self.item_desc, stretch=3)
        add_row.addWidget(self.item_cant)
        add_row.addWidget(self.item_precio)
        add_row.addWidget(btn_add)
        add_row.addWidget(btn_del)
        layout.addLayout(add_row)

        root.addWidget(group_items)

        # Ítem por defecto si la tabla está vacía
        self._insertar_fila("Mantenimiento preventivo integral y soporte técnico de redes", 1, 800000)

    def _setup_footer_actions(self, root: QVBoxLayout):
        footer = QFrame()
        footer.setObjectName("footerBar")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(18, 12, 18, 12)

        # Total Indicator
        box_total = QVBoxLayout()
        box_total.setSpacing(1)
        lbl_cap = QLabel("TOTAL GENERAL LIQUIDADO")
        lbl_cap.setObjectName("totalCaption")
        self.lbl_total_val = QLabel("$0 COP")
        self.lbl_total_val.setObjectName("totalValue")
        box_total.addWidget(lbl_cap)
        box_total.addWidget(self.lbl_total_val)
        footer_layout.addLayout(box_total)

        footer_layout.addStretch()

        # Action Buttons
        btn_excel = QPushButton("📊 Exportar Excel (.xlsx)")
        btn_excel.setObjectName("btnExcel")
        btn_excel.setCursor(Qt.PointingHandCursor)
        btn_excel.clicked.connect(self.exportar_excel)

        btn_gen_cot = QPushButton("📄 Generar Cotización (PDF)")
        btn_gen_cot.setObjectName("btnGenerate")
        btn_gen_cot.setCursor(Qt.PointingHandCursor)
        btn_gen_cot.clicked.connect(self.generar_cotizacion_pdf)

        btn_gen_cc = QPushButton("💳 Generar Cuenta de Cobro (PDF)")
        btn_gen_cc.setObjectName("btnGenerate")
        btn_gen_cc.setCursor(Qt.PointingHandCursor)
        btn_gen_cc.clicked.connect(self.generar_cuenta_cobro_pdf)

        footer_layout.addWidget(btn_excel)
        footer_layout.addWidget(btn_gen_cot)
        footer_layout.addWidget(btn_gen_cc)

        root.addWidget(footer)
        self.actualizar_total_ui()

    def _regenerar_concepto(self):
        contrato = self.input_num_contrato.text().strip() or "N° s/n"
        periodo = self.input_periodo_largo.text().strip() or self.input_periodo.text().strip()
        objeto = self.input_objeto_contrato.text().strip()
        texto = (
            f"Por concepto de pago por la prestación de servicios en cumplimiento del Contrato "
            f"Nº {contrato}, durante el período comprendido del {periodo}, cuyo objeto contractual "
            f"es: {objeto}"
        )
        self.input_concepto_cobro.setPlainText(texto)

    def _insertar_fila(self, desc: str, cant: int, precio: float):
        row = self.table.rowCount()
        self.table.insertRow(row)

        item_desc = QTableWidgetItem(desc)
        item_cant = QTableWidgetItem(str(cant))
        item_cant.setTextAlignment(Qt.AlignCenter)
        item_precio = QTableWidgetItem(formato_moneda_colombiana(precio))
        item_precio.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        item_total = QTableWidgetItem(formato_moneda_colombiana(precio * cant))
        item_total.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        item_total.setFlags(item_total.flags() & ~Qt.ItemIsEditable)

        self.table.setItem(row, 0, item_desc)
        self.table.setItem(row, 1, item_cant)
        self.table.setItem(row, 2, item_precio)
        self.table.setItem(row, 3, item_total)

    def agregar_item(self):
        desc = self.item_desc.text().strip()
        if not desc:
            QMessageBox.warning(self, "Atención", "Por favor ingresa una descripción para el ítem.")
            self.item_desc.setFocus()
            return

        cant = self.item_cant.value()
        precio = self.item_precio.value()
        self._insertar_fila(desc, cant, precio)

        self.item_desc.clear()
        self.item_cant.setValue(1)
        self.item_desc.setFocus()
        self.actualizar_total_ui()

    def eliminar_item(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)
            self.actualizar_total_ui()
        else:
            QMessageBox.information(self, "Aviso", "Selecciona una fila para eliminar.")

    def _obtener_items(self) -> list[ItemCotizacion]:
        items: list[ItemCotizacion] = []
        for r in range(self.table.rowCount()):
            desc = self.table.item(r, 0).text() if self.table.item(r, 0) else ""
            try:
                cant = int(self.table.item(r, 1).text()) if self.table.item(r, 1) else 1
            except ValueError:
                cant = 1
            val_u_str = self.table.item(r, 2).text() if self.table.item(r, 2) else "0"
            val_u = parsear_valor_moneda(val_u_str)
            items.append(ItemCotizacion(descripcion=desc, cantidad=cant, precio_unitario=val_u))
        return items

    def calcular_total(self) -> float:
        return sum(item.total for item in self._obtener_items())

    def actualizar_total_ui(self, *_):
        if self._actualizando:
            return
        self._actualizando = True
        try:
            total = 0.0
            for r in range(self.table.rowCount()):
                try:
                    cant = int(self.table.item(r, 1).text()) if self.table.item(r, 1) else 1
                except ValueError:
                    cant = 1
                val_u = parsear_valor_moneda(self.table.item(r, 2).text() if self.table.item(r, 2) else "0")
                row_total = val_u * cant
                total += row_total
                total_item = self.table.item(r, 3)
                if total_item:
                    total_item.setText(formato_moneda_colombiana(row_total))

            self.lbl_total_val.setText(f"{formato_moneda_colombiana(total, con_cop=True)}")
        finally:
            self._actualizando = False

    def generar_cotizacion_pdf(self):
        items = self._obtener_items()
        if not items:
            QMessageBox.warning(self, "Advertencia", "Añade al menos un ítem a la propuesta.")
            return

        cliente_sani = sanitizar_nombre_archivo(self.input_cliente.text())
        fecha_sani = sanitizar_nombre_archivo(self.input_fecha.text())
        nombre_defecto = f"Cotizacion_{cliente_sani}_{fecha_sani}.pdf"

        filepath, _ = QFileDialog.getSaveFileName(self, "Guardar Cotización PDF", nombre_defecto, "PDF Files (*.pdf)")
        if not filepath:
            return
        if not filepath.endswith(".pdf"):
            filepath += ".pdf"

        datos = DatosCotizacion(
            cliente=self.input_cliente.text().strip(),
            emisor=self.input_emisor.text().strip(),
            rut_emisor=self.input_rut.text().strip(),
            fecha=self.input_fecha.text().strip(),
            forma_pago=self.combo_pago.currentText(),
            objetivo_servicio=self.input_objetivo.text().strip(),
            detalle_servicios=self.input_detalle.toPlainText().strip(),
            items=items
        )

        html_content = render_cotizacion_html(datos)
        self._current_doc_type = "Cotización"
        self.pdf_service.exportar_pdf(html_content, filepath, self._on_pdf_generado)

    def generar_cuenta_cobro_pdf(self):
        items = self._obtener_items()
        if not items:
            QMessageBox.warning(self, "Advertencia", "Añade al menos un ítem a la cuenta de cobro.")
            return

        num_cuenta = self.input_num_cuenta.text().strip() or "001"
        cliente_sani = sanitizar_nombre_archivo(self.input_cliente.text())
        nombre_defecto = f"Cuenta_Cobro_{num_cuenta}_{cliente_sani}.pdf"

        filepath, _ = QFileDialog.getSaveFileName(self, "Guardar Cuenta de Cobro PDF", nombre_defecto, "PDF Files (*.pdf)")
        if not filepath:
            return
        if not filepath.endswith(".pdf"):
            filepath += ".pdf"

        firma_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "firma.png")

        datos = DatosCuentaCobro(
            num_cuenta=num_cuenta,
            num_contrato=self.input_num_contrato.text().strip(),
            periodo_ejecucion=self.input_periodo.text().strip(),
            periodo_largo=self.input_periodo_largo.text().strip(),
            objeto_contrato=self.input_objeto_contrato.text().strip(),
            concepto_cobro=self.input_concepto_cobro.toPlainText().strip(),
            cliente=self.input_cliente.text().strip(),
            nit_cliente=self.input_nit_cliente.text().strip(),
            ciudad_cliente=self.input_ciudad_cliente.text().strip(),
            emisor=self.input_emisor.text().strip(),
            rut_emisor=self.input_rut.text().strip(),
            lugar_expedicion=self.input_lugar_cc.text().strip(),
            telefono=self.input_telefono.text().strip(),
            email=self.input_email.text().strip(),
            cargo=self.input_cargo.text().strip(),
            banco=self.combo_banco.currentText().strip(),
            tipo_cuenta=self.combo_tipo_cuenta.currentText().strip(),
            numero_cuenta=self.input_num_cuenta_banco.text().strip(),
            titular_cuenta=self.input_titular_cuenta.text().strip(),
            incluir_tributario=self.check_tributario.isChecked(),
            incluir_firma=self.check_firma.isChecked(),
            ruta_firma=firma_path if os.path.exists(firma_path) else None,
            items=items
        )

        # Autoincrementar consecutivo para el siguiente documento
        nuevo_consecutivo = incrementar_consecutivo(num_cuenta)
        self.input_num_cuenta.setText(nuevo_consecutivo)
        self.config["consecutivo_cuenta"] = nuevo_consecutivo
        self._guardar_configuracion_actual()

        html_content = render_cuenta_cobro_html(datos)
        self._current_doc_type = "Cuenta de Cobro"
        self.pdf_service.exportar_pdf(html_content, filepath, self._on_pdf_generado)

    def exportar_excel(self):
        items = self._obtener_items()
        if not items:
            QMessageBox.warning(self, "Advertencia", "Añade al menos un ítem para exportar a Excel.")
            return

        cliente_sani = sanitizar_nombre_archivo(self.input_cliente.text())
        nombre_defecto = f"Propuesta_{cliente_sani}.xlsx"

        filepath, _ = QFileDialog.getSaveFileName(self, "Guardar Libro de Excel", nombre_defecto, "Excel Files (*.xlsx)")
        if not filepath:
            return
        if not filepath.endswith(".xlsx"):
            filepath += ".xlsx"

        datos = DatosCotizacion(
            cliente=self.input_cliente.text().strip(),
            emisor=self.input_emisor.text().strip(),
            rut_emisor=self.input_rut.text().strip(),
            fecha=self.input_fecha.text().strip(),
            forma_pago=self.combo_pago.currentText(),
            objetivo_servicio=self.input_objetivo.text().strip(),
            detalle_servicios=self.input_detalle.toPlainText().strip(),
            items=items
        )

        try:
            exportar_cotizacion_excel(datos, filepath)
            msg = QMessageBox(self)
            msg.setWindowTitle("Excel Exportado con Éxito")
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"¡Libro de Excel profesional guardado correctamente en:\n{filepath}")
            btn_abrir = msg.addButton("Abrir Excel", QMessageBox.AcceptRole)
            btn_cerrar = msg.addButton("Aceptar", QMessageBox.RejectRole)
            msg.setDefaultButton(btn_abrir)
            msg.exec_()
            if msg.clickedButton() == btn_abrir:
                os.startfile(os.path.normpath(filepath))
        except Exception as e:
            QMessageBox.critical(self, "Error al Exportar Excel", f"No se pudo guardar el archivo: {e}")

    def _on_pdf_generado(self, filepath: str, success: bool):
        if success:
            tipo_doc = self._current_doc_type
            msg = QMessageBox(self)
            msg.setWindowTitle(f"{tipo_doc} Generado")
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"¡{tipo_doc} guardado perfectamente en:\n{filepath}")
            btn_abrir = msg.addButton("Abrir PDF", QMessageBox.AcceptRole)
            btn_cerrar = msg.addButton("Aceptar", QMessageBox.RejectRole)
            msg.setDefaultButton(btn_abrir)
            msg.exec_()
            if msg.clickedButton() == btn_abrir:
                try:
                    os.startfile(os.path.normpath(filepath))
                except Exception as e:
                    QMessageBox.warning(self, "Aviso", f"No se pudo abrir el visor automáticamente: {e}")
        else:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al generar el PDF ({self._current_doc_type}).")

    def _guardar_configuracion_actual(self):
        self.config["cliente_defecto"] = self.input_cliente.text().strip()
        self.config["nit_cliente"] = self.input_nit_cliente.text().strip()
        self.config["ciudad_cliente"] = self.input_ciudad_cliente.text().strip()
        self.config["emisor"] = self.input_emisor.text().strip()
        self.config["rut"] = self.input_rut.text().strip()
        self.config["lugar_expedicion"] = self.input_lugar_cc.text().strip()
        self.config["telefono"] = self.input_telefono.text().strip()
        self.config["email"] = self.input_email.text().strip()
        self.config["cargo"] = self.input_cargo.text().strip()
        self.config["num_contrato"] = self.input_num_contrato.text().strip()
        self.config["periodo_ejecucion"] = self.input_periodo.text().strip()
        self.config["periodo_largo"] = self.input_periodo_largo.text().strip()
        self.config["objeto_contrato"] = self.input_objeto_contrato.text().strip()
        self.config["banco"] = self.combo_banco.currentText().strip()
        self.config["tipo_cuenta"] = self.combo_tipo_cuenta.currentText().strip()
        self.config["numero_cuenta"] = self.input_num_cuenta_banco.text().strip()
        self.config["titular"] = self.input_titular_cuenta.text().strip()
        self.config["incluir_tributario"] = self.check_tributario.isChecked()
        self.config["incluir_firma"] = self.check_firma.isChecked()
        guardar_configuracion(self.config)

    def closeEvent(self, event):
        self._guardar_configuracion_actual()
        super().closeEvent(event)
