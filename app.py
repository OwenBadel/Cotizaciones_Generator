"""
Generador Profesional de Cotizaciones y Cuentas de Cobro TI — Owen Badel Hooker
Módulo de compatibilidad retroactiva.
Para ejecutar la arquitectura modular, ver `main.py`.
"""

import sys
from PyQt5.QtCore import Qt, QCoreApplication

# Requisito indispensable de QtWebEngine antes de inicializar QCoreApplication / QApplication
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

from PyQt5.QtWebEngineWidgets import QWebEngineView  # noqa: F401 - Preinicialización de WebEngine
from PyQt5.QtWidgets import QApplication
from ui.main_window import GeneradorCotizacionesWindow

# Alias de compatibilidad para scripts o tests antiguos
GeneradorCotizaciones = GeneradorCotizacionesWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("GeneradorCotizacionesTI")
    app.setOrganizationName("OwenBadel")
    window = GeneradorCotizacionesWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
