"""
Estilos visuales modernos y ergonómicos en QSS para la suite de cotizaciones y cuentas de cobro.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

APP_QSS = """
* {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
    color: #1e293b;
}

QMainWindow, QWidget#central {
    background-color: #f1f5f9;
}

/* ---------- Encabezado de la app ---------- */
QFrame#appHeader {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f172a, stop:1 #1e3a8a);
    border-radius: 12px;
}
QLabel#appTitle {
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
QLabel#appSubtitle {
    color: #93c5fd;
    font-size: 12px;
}

/* ---------- Pestañas (QTabWidget) ---------- */
QTabWidget::pane {
    border: 1px solid #cbd5e1;
    background-color: #ffffff;
    border-radius: 12px;
    top: -1px;
    padding: 10px;
}
QTabBar::tab {
    background-color: #e2e8f0;
    color: #475569;
    font-weight: 600;
    font-size: 13px;
    padding: 8px 18px;
    margin-right: 6px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border: 1px solid #cbd5e1;
    border-bottom: none;
    min-width: 140px;
}
QTabBar::tab:selected {
    background-color: #ffffff;
    color: #1e3a8a;
    border-color: #cbd5e1;
    border-bottom: 2px solid #ffffff;
    font-weight: 700;
}
QTabBar::tab:hover:!selected {
    background-color: #cbd5e1;
    color: #0f172a;
}

/* ---------- Agrupadores (QGroupBox) ---------- */
QGroupBox {
    font-weight: 700;
    font-size: 12px;
    color: #1e3a8a;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    margin-top: 10px;
    padding-top: 14px;
    background-color: #f8fafc;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 6px;
    background-color: #f8fafc;
}

/* ---------- Controles de Formulario ---------- */
QLabel {
    color: #475569;
    font-weight: 500;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px 10px;
    color: #0f172a;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1.5px solid #2563eb;
    background-color: #ffffff;
}
QLineEdit:hover, QTextEdit:hover, QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border-color: #94a3b8;
}

/* ---------- Botones ---------- */
QPushButton {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 7px 14px;
    font-weight: 600;
    color: #334155;
}
QPushButton:hover {
    background-color: #f1f5f9;
    border-color: #94a3b8;
    color: #0f172a;
}
QPushButton:pressed {
    background-color: #e2e8f0;
}

/* Botón Añadir Ítem */
QPushButton#btnAdd {
    background-color: #2563eb;
    border: 1px solid #1d4ed8;
    color: #ffffff;
    font-weight: 700;
    padding: 7px 16px;
}
QPushButton#btnAdd:hover {
    background-color: #1d4ed8;
}
QPushButton#btnAdd:pressed {
    background-color: #1e40af;
}

/* Botón Eliminar Ítem */
QPushButton#btnDelete {
    background-color: #fee2e2;
    border: 1px solid #fca5a5;
    color: #dc2626;
    font-weight: 600;
    padding: 7px 12px;
}
QPushButton#btnDelete:hover {
    background-color: #fecaca;
    border-color: #f87171;
    color: #b91c1c;
}
QPushButton#btnDelete:pressed {
    background-color: #fca5a5;
}

/* Botón Generar PDF Primario */
QPushButton#btnGenerate {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e3a8a, stop:1 #2563eb);
    border: none;
    border-radius: 8px;
    color: #ffffff;
    font-size: 14px;
    font-weight: 700;
    padding: 10px 24px;
    min-height: 22px;
}
QPushButton#btnGenerate:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #172554, stop:1 #1d4ed8);
}
QPushButton#btnGenerate:pressed {
    background-color: #1e3a8a;
}

/* Botón Exportar a Excel */
QPushButton#btnExcel {
    background-color: #107c41;
    border: 1px solid #0b5a2f;
    border-radius: 8px;
    color: #ffffff;
    font-size: 13px;
    font-weight: 700;
    padding: 9px 18px;
    min-height: 22px;
}
QPushButton#btnExcel:hover {
    background-color: #0b5a2f;
}
QPushButton#btnExcel:pressed {
    background-color: #06391d;
}

/* ---------- Tabla de Ítems ---------- */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    gridline-color: #f1f5f9;
    selection-background-color: #dbeafe;
    selection-color: #1e3a8a;
}
QHeaderView::section {
    background-color: #1e293b;
    color: #ffffff;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 8px 10px;
    border: none;
    border-right: 1px solid #334155;
}
QHeaderView::section:last {
    border-right: none;
}
QTableWidget::item {
    padding: 4px 8px;
    border-bottom: 1px solid #f1f5f9;
}
QTableWidget::item:selected {
    background-color: #dbeafe;
    color: #1e3a8a;
    font-weight: 600;
}

/* ---------- Barra de Scroll ---------- */
QScrollBar:vertical {
    border: none;
    background: #f1f5f9;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #94a3b8;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #64748b;
}

/* ---------- Pie / Total ---------- */
QFrame#footerBar {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}
QLabel#totalCaption {
    color: #64748b;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
}
QLabel#totalValue {
    color: #1e3a8a;
    font-size: 21px;
    font-weight: 800;
}
"""
