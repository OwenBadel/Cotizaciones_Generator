"""
Servicio desacoplado de renderizado de HTML a PDF vectorial de alta resolución mediante Qt WebEngine.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

from typing import Callable, Optional
from PyQt5.QtCore import QMarginsF, QObject, pyqtSignal
from PyQt5.QtGui import QPageLayout, QPageSize
from PyQt5.QtWebEngineWidgets import QWebEngineView


class PDFRenderService(QObject):
    """Maneja el ciclo de vida del renderizado de HTML hacia archivos PDF estándar A4."""
    finished = pyqtSignal(str, bool)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.web_view: Optional[QWebEngineView] = None
        self.target_filepath: str = ""
        self._callback: Optional[Callable[[str, bool], None]] = None

    def exportar_pdf(
        self,
        html_content: str,
        output_filepath: str,
        callback: Optional[Callable[[str, bool], None]] = None
    ):
        """Inicia el proceso asíncrono de renderizado de página a PDF."""
        self.target_filepath = output_filepath
        self._callback = callback

        # Instanciar QWebEngineView para cada renderizado limpio
        self.web_view = QWebEngineView()
        self.web_view.setHtml(html_content)
        self.web_view.loadFinished.connect(self._on_html_loaded)

    def _on_html_loaded(self, success: bool):
        if not success or not self.web_view:
            self._notificar_resultado(self.target_filepath, False)
            return

        margenes = QMarginsF(14, 16, 14, 16)
        layout_a4 = QPageLayout(
            QPageSize(QPageSize.A4),
            QPageLayout.Portrait,
            margenes,
            QPageLayout.Millimeter
        )
        self.web_view.page().printToPdf(self.target_filepath, layout_a4)
        self.web_view.page().pdfPrintingFinished.connect(self._on_pdf_printed)

    def _on_pdf_printed(self, filepath: str, success: bool):
        self._notificar_resultado(filepath, success)

    def _notificar_resultado(self, filepath: str, success: bool):
        self.finished.emit(filepath, success)
        if self._callback:
            self._callback(filepath, success)
        # Liberar recurso web_view
        self.web_view = None
