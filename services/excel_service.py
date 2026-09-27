"""
Servicio de exportación de cotizaciones y propuestas técnicas a Excel (.xlsx).
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from core.models import DatosCotizacion, DatosCuentaCobro


def exportar_cotizacion_excel(datos: DatosCotizacion, ruta_salida: str) -> bool:
    """Genera un libro de Excel (.xlsx) con diseño corporativo y formato de moneda."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Propuesta TI"

    # Fuentes y estilos
    font_titulo = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
    font_sub = Font(name="Segoe UI", size=10, italic=True, color="93C5FD")
    font_header = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    font_meta_lbl = Font(name="Segoe UI", size=9, bold=True, color="475569")
    font_meta_val = Font(name="Segoe UI", size=10, bold=True, color="0F172A")
    font_row = Font(name="Segoe UI", size=10, color="334155")
    font_total = Font(name="Segoe UI", size=11, bold=True, color="1E3A8A")

    fill_banner = PatternFill(start_color="0F2A59", end_color="0F2A59", fill_type="solid")
    fill_header = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    fill_total = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")

    thin_border = Border(
        left=Side(style="thin", color="E2E8F0"),
        right=Side(style="thin", color="E2E8F0"),
        top=Side(style="thin", color="E2E8F0"),
        bottom=Side(style="thin", color="E2E8F0"),
    )
    total_top_border = Side(style="medium", color="2563EB")
    border_total = Border(top=total_top_border, bottom=Side(style="double", color="2563EB"))

    # 1. Encabezado Banner
    ws.merge_cells("A1:E1")
    ws["A1"] = "PROPUESTA TÉCNICA Y ECONÓMICA DE SERVICIOS TI"
    ws["A1"].font = font_titulo
    ws["A1"].fill = fill_banner
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 32

    ws.merge_cells("A2:E2")
    ws["A2"] = f"Preparado por: {datos.emisor} | NIT/RUT: {datos.rut_emisor}"
    ws["A2"].font = font_sub
    ws["A2"].fill = fill_banner
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 20

    # 2. Metadatos del Cliente y Fecha
    ws.append([])  # Fila 3 en blanco
    ws["A4"] = "Cliente:"
    ws["A4"].font = font_meta_lbl
    ws["B4"] = datos.cliente
    ws["B4"].font = font_meta_val

    ws["D4"] = "Fecha:"
    ws["D4"].font = font_meta_lbl
    ws["E4"] = datos.fecha
    ws["E4"].font = font_meta_val

    ws["A5"] = "Forma de Pago:"
    ws["A5"].font = font_meta_lbl
    ws["B5"] = datos.forma_pago
    ws["B5"].font = font_meta_val

    # 3. Tabla de Ítems
    ws.append([])  # Fila 6 en blanco
    headers = ["Ítem", "Descripción del Servicio", "Cantidad", "Valor Unitario", "Valor Total"]
    ws.append(headers)
    fila_header = ws.max_row
    ws.row_dimensions[fila_header].height = 24

    for col_idx in range(1, 6):
        celda = ws.cell(row=fila_header, column=col_idx)
        celda.font = font_header
        celda.fill = fill_header
        celda.alignment = Alignment(horizontal="center" if col_idx in (1, 3) else ("right" if col_idx >= 4 else "left"), vertical="center")

    # Filas de datos
    fila_inicio_datos = ws.max_row + 1
    for idx, item in enumerate(datos.items, 1):
        fila = [idx, item.descripcion, item.cantidad, item.precio_unitario, item.total]
        ws.append(fila)
        curr_row = ws.max_row
        ws.row_dimensions[curr_row].height = 22

        for col_idx in range(1, 6):
            c = ws.cell(row=curr_row, column=col_idx)
            c.font = font_row
            c.border = thin_border
            if idx % 2 == 0:
                c.fill = fill_zebra

            if col_idx in (1, 3):
                c.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx in (4, 5):
                c.number_format = '"$"#,##0'
                c.alignment = Alignment(horizontal="right", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")

    # Fila de Total
    fila_fin_datos = ws.max_row
    ws.append(["", "TOTAL GENERAL (COP)", "", "", f"=SUM(E{fila_inicio_datos}:E{fila_fin_datos})"])
    fila_total = ws.max_row
    ws.row_dimensions[fila_total].height = 26

    for col_idx in range(1, 6):
        c = ws.cell(row=fila_total, column=col_idx)
        c.font = font_total
        c.fill = fill_total
        c.border = border_total
        if col_idx in (2, 5):
            c.alignment = Alignment(horizontal="right", vertical="center")
        if col_idx == 5:
            c.number_format = '"$"#,##0 "COP"'

    # Ajuste de ancho de columnas
    anchos = {"A": 10, "B": 48, "C": 14, "D": 22, "E": 24}
    for col_letra, ancho in anchos.items():
        ws.column_dimensions[col_letra].width = ancho

    wb.save(ruta_salida)
    return True
