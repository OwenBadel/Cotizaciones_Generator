"""
Servicio de exportación de cotizaciones y cuentas de cobro a libros corporativos de Excel (.xlsx).
Diseñado bajo estándares de ingeniería y finanzas corporativas.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from core.models import DatosCotizacion, DatosCuentaCobro


def exportar_cotizacion_excel(datos: DatosCotizacion, ruta_salida: str) -> bool:
    """Genera un libro de Excel (.xlsx) con liquidación comercial detallada (descuento, IVA, total)."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Propuesta Económica TI"

    # Fuentes y paleta corporativa
    font_titulo = Font(name="Segoe UI", size=13, bold=True, color="FFFFFF")
    font_sub = Font(name="Segoe UI", size=9, italic=True, color="93C5FD")
    font_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    font_meta_lbl = Font(name="Segoe UI", size=9, bold=True, color="475569")
    font_meta_val = Font(name="Segoe UI", size=9, bold=True, color="0F172A")
    font_row = Font(name="Segoe UI", size=9, color="334155")
    font_subtotal = Font(name="Segoe UI", size=9, bold=True, color="475569")
    font_descuento = Font(name="Segoe UI", size=9, bold=True, color="BE123C")
    font_iva = Font(name="Segoe UI", size=9, bold=True, color="15803D")
    font_total = Font(name="Segoe UI", size=11, bold=True, color="0F2A59")

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
    border_total = Border(
        top=Side(style="medium", color="2563EB"),
        bottom=Side(style="double", color="2563EB")
    )

    # 1. Banner
    ws.merge_cells("A1:E1")
    ws["A1"] = f"PROPUESTA TÉCNICA Y ECONÓMICA DE SERVICIOS TI — {datos.consecutivo}"
    ws["A1"].font = font_titulo
    ws["A1"].fill = fill_banner
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:E2")
    ws["A2"] = f"Emisor: {datos.emisor} | NIT/RUT: {datos.rut_emisor} | Validez: {datos.vigencia_dias} días"
    ws["A2"].font = font_sub
    ws["A2"].fill = fill_banner
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 18

    # 2. Metadatos
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

    # 3. Encabezados de Tabla
    ws.append([])  # Fila 6 en blanco
    headers = ["Ítem", "Descripción del Servicio", "Cantidad", "Valor Unitario", "Valor Total"]
    ws.append(headers)
    fila_header = ws.max_row
    ws.row_dimensions[fila_header].height = 22

    for col_idx in range(1, 6):
        celda = ws.cell(row=fila_header, column=col_idx)
        celda.font = font_header
        celda.fill = fill_header
        celda.alignment = Alignment(horizontal="center" if col_idx in (1, 3) else ("right" if col_idx >= 4 else "left"), vertical="center")

    # Filas de ítems
    fila_inicio_datos = ws.max_row + 1
    for idx, item in enumerate(datos.items, 1):
        fila = [idx, item.descripcion, item.cantidad, item.precio_unitario, item.total]
        ws.append(fila)
        curr_row = ws.max_row
        ws.row_dimensions[curr_row].height = 20

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

    fila_fin_datos = ws.max_row

    # 4. Liquidación Financiera
    # Subtotal
    if datos.descuento_porcentaje > 0 or datos.aplicar_iva:
        ws.append(["", "", "", "SUBTOTAL:", f"=SUM(E{fila_inicio_datos}:E{fila_fin_datos})"])
        f_sub = ws.max_row
        ws.cell(row=f_sub, column=4).font = font_subtotal
        ws.cell(row=f_sub, column=4).alignment = Alignment(horizontal="right", vertical="center")
        c_sub = ws.cell(row=f_sub, column=5)
        c_sub.font = font_subtotal
        c_sub.number_format = '"$"#,##0'
        c_sub.alignment = Alignment(horizontal="right", vertical="center")

    # Descuento
    if datos.descuento_porcentaje > 0:
        ws.append(["", "", "", f"DESCUENTO ({datos.descuento_porcentaje:.1f}%):", -datos.descuento_valor])
        f_desc = ws.max_row
        ws.cell(row=f_desc, column=4).font = font_descuento
        ws.cell(row=f_desc, column=4).alignment = Alignment(horizontal="right", vertical="center")
        c_desc = ws.cell(row=f_desc, column=5)
        c_desc.font = font_descuento
        c_desc.number_format = '"$"#,##0'
        c_desc.alignment = Alignment(horizontal="right", vertical="center")

    # IVA
    if datos.aplicar_iva:
        ws.append(["", "", "", f"IVA ({datos.iva_porcentaje:.0f}%):", datos.iva_valor])
        f_iva = ws.max_row
        ws.cell(row=f_iva, column=4).font = font_iva
        ws.cell(row=f_iva, column=4).alignment = Alignment(horizontal="right", vertical="center")
        c_iva = ws.cell(row=f_iva, column=5)
        c_iva.font = font_iva
        c_iva.number_format = '"$"#,##0'
        c_iva.alignment = Alignment(horizontal="right", vertical="center")

    # Total General
    ws.append(["", "", "", "TOTAL GENERAL (COP):", datos.total_general])
    fila_total = ws.max_row
    ws.row_dimensions[fila_total].height = 24

    for col_idx in range(1, 6):
        c = ws.cell(row=fila_total, column=col_idx)
        c.font = font_total
        c.fill = fill_total
        c.border = border_total
        if col_idx in (4, 5):
            c.alignment = Alignment(horizontal="right", vertical="center")
        if col_idx == 5:
            c.number_format = '"$"#,##0 "COP"'

    # Ajuste de ancho de columnas
    anchos = {"A": 8, "B": 50, "C": 12, "D": 22, "E": 24}
    for col_letra, ancho in anchos.items():
        ws.column_dimensions[col_letra].width = ancho

    wb.save(ruta_salida)
    return True


def exportar_cuenta_cobro_excel(datos: DatosCuentaCobro, ruta_salida: str) -> bool:
    """Genera un libro de Excel (.xlsx) para Cuenta de Cobro con retenciones y datos bancarios."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Cuenta Cobro {datos.num_cuenta}"

    font_titulo = Font(name="Segoe UI", size=13, bold=True, color="FFFFFF")
    font_sub = Font(name="Segoe UI", size=9, italic=True, color="93C5FD")
    font_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    font_meta_lbl = Font(name="Segoe UI", size=9, bold=True, color="475569")
    font_meta_val = Font(name="Segoe UI", size=9, bold=True, color="0F172A")
    font_row = Font(name="Segoe UI", size=9, color="334155")
    font_ret = Font(name="Segoe UI", size=9, bold=True, color="BE123C")
    font_total = Font(name="Segoe UI", size=11, bold=True, color="0F2A59")
    font_bank = Font(name="Segoe UI", size=9, color="1E3A8A")

    fill_banner = PatternFill(start_color="0F2A59", end_color="0F2A59", fill_type="solid")
    fill_header = PatternFill(start_color="112340", end_color="112340", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    fill_total = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")
    fill_bank = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")

    thin_border = Border(
        left=Side(style="thin", color="E2E8F0"),
        right=Side(style="thin", color="E2E8F0"),
        top=Side(style="thin", color="E2E8F0"),
        bottom=Side(style="thin", color="E2E8F0"),
    )
    border_total = Border(
        top=Side(style="medium", color="2563EB"),
        bottom=Side(style="double", color="2563EB")
    )

    # 1. Banner
    ws.merge_cells("A1:E1")
    ws["A1"] = f"CUENTA DE COBRO N° {datos.num_cuenta}"
    ws["A1"].font = font_titulo
    ws["A1"].fill = fill_banner
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:E2")
    ws["A2"] = f"Contrato de Prestación de Servicios Nº {datos.num_contrato} | Período: {datos.periodo_ejecucion}"
    ws["A2"].font = font_sub
    ws["A2"].fill = fill_banner
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 18

    # 2. Metadatos
    ws["A4"] = "Debe a:"
    ws["A4"].font = font_meta_lbl
    ws["B4"] = f"{datos.emisor} (C.C. {datos.rut_emisor})"
    ws["B4"].font = font_meta_val

    ws["D4"] = "A favor de:"
    ws["D4"].font = font_meta_lbl
    ws["E4"] = f"{datos.cliente} (NIT {datos.nit_cliente})"
    ws["E4"].font = font_meta_val

    # 3. Concepto
    ws["A5"] = "Concepto:"
    ws["A5"].font = font_meta_lbl
    ws.merge_cells("B5:E5")
    ws["B5"] = datos.concepto_cobro
    ws["B5"].font = font_row
    ws["B5"].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[5].height = 36

    # 4. Tabla de Ítems
    ws.append([])  # Fila 6 en blanco
    headers = ["Ítem", "Descripción del Servicio", "Cantidad", "Valor Unitario", "Valor Total"]
    ws.append(headers)
    fila_header = ws.max_row
    ws.row_dimensions[fila_header].height = 22

    for col_idx in range(1, 6):
        celda = ws.cell(row=fila_header, column=col_idx)
        celda.font = font_header
        celda.fill = fill_header
        celda.alignment = Alignment(horizontal="center" if col_idx in (1, 3) else ("right" if col_idx >= 4 else "left"), vertical="center")

    fila_inicio_datos = ws.max_row + 1
    for idx, item in enumerate(datos.items, 1):
        ws.append([idx, item.descripcion, item.cantidad, item.precio_unitario, item.total])
        curr_row = ws.max_row
        ws.row_dimensions[curr_row].height = 20

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

    fila_fin_datos = ws.max_row

    # 5. Liquidación y Retenciones
    if datos.aplicar_retefuente or datos.aplicar_reteica:
        ws.append(["", "", "", "VALOR BRUTO:", f"=SUM(E{fila_inicio_datos}:E{fila_fin_datos})"])
        f_bruto = ws.max_row
        ws.cell(row=f_bruto, column=4).font = font_meta_lbl
        ws.cell(row=f_bruto, column=4).alignment = Alignment(horizontal="right", vertical="center")
        c_bruto = ws.cell(row=f_bruto, column=5)
        c_bruto.font = font_meta_val
        c_bruto.number_format = '"$"#,##0'
        c_bruto.alignment = Alignment(horizontal="right", vertical="center")

    if datos.aplicar_retefuente:
        ws.append(["", "", "", f"RETEFUENTE ({datos.retefuente_porcentaje:.1f}%):", -datos.retefuente_valor])
        f_ret = ws.max_row
        ws.cell(row=f_ret, column=4).font = font_ret
        ws.cell(row=f_ret, column=4).alignment = Alignment(horizontal="right", vertical="center")
        c_ret = ws.cell(row=f_ret, column=5)
        c_ret.font = font_ret
        c_ret.number_format = '"$"#,##0'
        c_ret.alignment = Alignment(horizontal="right", vertical="center")

    if datos.aplicar_reteica:
        ws.append(["", "", "", f"RETEICA ({datos.reteica_porcentaje:.3f}%):", -datos.reteica_valor])
        f_ica = ws.max_row
        ws.cell(row=f_ica, column=4).font = font_ret
        ws.cell(row=f_ica, column=4).alignment = Alignment(horizontal="right", vertical="center")
        c_ica = ws.cell(row=f_ica, column=5)
        c_ica.font = font_ret
        c_ica.number_format = '"$"#,##0'
        c_ica.alignment = Alignment(horizontal="right", vertical="center")

    # Total Neto
    ws.append(["", "", "", "TOTAL NETO A PAGAR:", datos.total_general])
    fila_total = ws.max_row
    ws.row_dimensions[fila_total].height = 24

    for col_idx in range(1, 6):
        c = ws.cell(row=fila_total, column=col_idx)
        c.font = font_total
        c.fill = fill_total
        c.border = border_total
        if col_idx in (4, 5):
            c.alignment = Alignment(horizontal="right", vertical="center")
        if col_idx == 5:
            c.number_format = '"$"#,##0 "COP"'

    # 6. Datos Bancarios
    ws.append([])
    f_banco = ws.max_row + 1
    ws.merge_cells(f"A{f_banco}:E{f_banco}")
    ws[f"A{f_banco}"] = f"DATOS DE CONSIGNACIÓN: {datos.banco} — Cuenta {datos.tipo_cuenta} N° {datos.numero_cuenta} | Titular: {datos.titular_cuenta}"
    ws[f"A{f_banco}"].font = font_bank
    ws[f"A{f_banco}"].fill = fill_bank
    ws[f"A{f_banco}"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[f_banco].height = 22

    anchos = {"A": 8, "B": 50, "C": 12, "D": 22, "E": 24}
    for col_letra, ancho in anchos.items():
        ws.column_dimensions[col_letra].width = ancho

    wb.save(ruta_salida)
    return True
