"""
Plantilla HTML/CSS de alta fidelidad para Cuenta de Cobro Oficial.
Soporta retenciones tributarias opcionales (Retefuente, ReteICA) y cálculo neto.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

import html
from datetime import datetime
from core.models import DatosCuentaCobro
from core.utils import obtener_imagen_base64


def render_cuenta_cobro_html(datos: DatosCuentaCobro, fecha_expedicion: str = None) -> str:
    """Renderiza el documento HTML/CSS imprimible para la Cuenta de Cobro."""
    if not fecha_expedicion:
        ahora = datetime.now()
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        fecha_expedicion = f"{ahora.day} de {meses[ahora.month - 1]} de {ahora.year}"

    # Filas de ítems
    rows_html = ""
    for idx, item in enumerate(datos.items, 1):
        rows_html += f"""
        <tr>
            <td class="text-center">{idx}</td>
            <td>{html.escape(item.descripcion)}</td>
            <td class="text-center">{item.cantidad}</td>
            <td class="text-right">{item.precio_unitario_formateado}</td>
            <td class="text-right">{item.total_formateado}</td>
        </tr>
        """

    # Filas de liquidación y retenciones
    filas_liquidacion_html = ""
    if datos.aplicar_retefuente or datos.aplicar_reteica:
        filas_liquidacion_html += f"""
        <tr class="subtotal-row">
            <td colspan="4" class="text-right">VALOR BRUTO</td>
            <td class="text-right">{datos.subtotal_bruto_formateado}</td>
        </tr>
        """

    if datos.aplicar_retefuente:
        filas_liquidacion_html += f"""
        <tr class="discount-row">
            <td colspan="4" class="text-right">RETENCIÓN EN LA FUENTE ({datos.retefuente_porcentaje:.1f}%)</td>
            <td class="text-right">-{datos.retefuente_formateado}</td>
        </tr>
        """

    if datos.aplicar_reteica:
        filas_liquidacion_html += f"""
        <tr class="discount-row">
            <td colspan="4" class="text-right">RETEICA ({datos.reteica_porcentaje:.3f}%)</td>
            <td class="text-right">-{datos.reteica_formateado}</td>
        </tr>
        """

    filas_liquidacion_html += f"""
    <tr class="total-row">
        <td colspan="4" class="text-right">TOTAL NETO A PAGAR</td>
        <td class="text-right">{datos.total_formateado} COP</td>
    </tr>
    """

    # Declaración tributaria
    seccion_tributaria_html = ""
    if datos.incluir_tributario:
        seccion_tributaria_html = f"""
        <div class="section-title">4. DECLARACIÓN TRIBUTARIA</div>
        <div class="tax-box">
            <p><strong>Manifiesto bajo la gravedad del juramento</strong> que pertenezco al régimen de <strong>No Responsables del Impuesto sobre las Ventas (IVA)</strong> de conformidad con el artículo 437 del Estatuto Tributario, por lo cual este documento soporte no causa dicho impuesto.</p>
        </div>
        """

    # Firma digital
    firma_b64 = ""
    if datos.incluir_firma and datos.ruta_firma:
        firma_b64 = obtener_imagen_base64(datos.ruta_firma)

    img_tag = f'<img src="{firma_b64}" alt="Firma" class="signature-img" />' if firma_b64 else '<div style="height: 38px;"></div>'

    bloque_firma_html = f"""
    <div class="signature-area">
        {img_tag}
        <div class="signature-rule"></div>
        <div class="signature-name">{html.escape(datos.emisor.upper())}</div>
        <div class="signature-meta">C.C. {html.escape(datos.rut_emisor)} {html.escape(datos.lugar_expedicion)}</div>
        <div class="signature-meta">Tel: {html.escape(datos.telefono)} | <span class="signature-email">{html.escape(datos.email)}</span></div>
        <div class="signature-meta">{html.escape(datos.cargo)}</div>
    </div>
    """

    concepto_html = html.escape(datos.concepto_cobro).replace('\n', '<br>')

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
    @page {{
        size: A4;
        margin: 14mm 16mm 14mm 16mm;
    }}
    *, *::before, *::after {{
        box-sizing: border-box;
    }}
    body {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1e293b;
        margin: 0;
        padding: 0;
        font-size: 9.5pt;
        line-height: 1.45;
        background-color: #ffffff;
    }}
    .header-banner {{
        background: #0f2a59;
        color: #ffffff;
        padding: 18px 24px;
        border-radius: 8px;
        margin-bottom: 16px;
    }}
    .header-title {{
        font-size: 19pt;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin: 0 0 5px 0;
        color: #ffffff;
        text-transform: uppercase;
    }}
    .header-subtitle {{
        font-size: 10pt;
        color: #93c5fd;
        font-weight: 500;
        margin: 0;
    }}
    .meta-grid {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 12px 0;
        margin-left: -12px;
        margin-right: -12px;
        margin-bottom: 14px;
    }}
    .meta-card {{
        background-color: #f8fafc;
        padding: 9px 13px;
        border-radius: 4px;
        border-left: 3.5px solid #2563eb;
        border-top: 1px solid #f1f5f9;
        border-right: 1px solid #f1f5f9;
        border-bottom: 1px solid #f1f5f9;
        min-height: 68px;
    }}
    .meta-label {{
        font-size: 7.5pt;
        text-transform: uppercase;
        color: #2563eb;
        font-weight: 700;
        letter-spacing: 0.3px;
        margin-bottom: 3px;
    }}
    .meta-value {{
        font-size: 9.5pt;
        color: #0f172a;
        font-weight: 700;
        margin-bottom: 2px;
    }}
    .meta-sub {{
        font-size: 8pt;
        color: #64748b;
        line-height: 1.35;
    }}
    .section-title {{
        font-size: 10.5pt;
        font-weight: 800;
        color: #1e3a8a;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-top: 13px;
        margin-bottom: 7px;
        padding-bottom: 3px;
        border-bottom: 1px solid #e2e8f0;
    }}
    .concept-box {{
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 11px 15px;
        font-size: 9pt;
        line-height: 1.5;
        color: #334155;
        margin-bottom: 14px;
    }}
    table.pricing-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 6px;
        margin-bottom: 6px;
        background: #ffffff;
    }}
    table.pricing-table thead th {{
        background-color: #112340;
        color: #ffffff;
        font-weight: 700;
        padding: 8px 10px;
        font-size: 8pt;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }}
    table.pricing-table td {{
        padding: 7px 10px;
        border-bottom: 1px solid #f1f5f9;
        color: #334155;
        font-size: 8.5pt;
    }}
    table.pricing-table tbody tr:nth-child(even) td {{
        background-color: #f8fafc;
    }}
    .text-center {{ text-align: center; }}
    .text-right {{ text-align: right; }}
    .subtotal-row td {{
        background-color: #f8fafc !important;
        font-weight: 600;
        color: #475569;
        font-size: 8.5pt;
    }}
    .discount-row td {{
        background-color: #fff1f2 !important;
        font-weight: 600;
        color: #be123c;
        font-size: 8.5pt;
    }}
    .total-row td {{
        background-color: #e8f1fd !important;
        font-weight: 800;
        color: #112340;
        font-size: 9.5pt;
        padding: 8px 10px;
        border-top: 1.5px solid #2563eb;
        border-bottom: 1.5px solid #2563eb;
    }}
    .valor-letras-bar {{
        font-size: 8pt;
        color: #64748b;
        margin-top: 6px;
        margin-bottom: 14px;
    }}
    .valor-letras-bar strong {{
        color: #475569;
    }}
    .valor-letras-bar span {{
        color: #1e293b;
        font-weight: 600;
    }}
    .bank-box {{
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #2563eb;
        border-radius: 6px;
        padding: 9px 15px;
        margin-bottom: 14px;
    }}
    .bank-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 9pt;
    }}
    .bank-table td {{
        padding: 2.5px 4px;
        vertical-align: middle;
    }}
    .bank-table td.lbl {{
        width: 160px;
        color: #475569;
        font-weight: 600;
    }}
    .bank-table td.val {{
        color: #1e293b;
    }}
    .bank-table td.val.bold {{
        font-weight: 700;
        color: #0f172a;
    }}
    .tax-box {{
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 4px solid #16a34a;
        border-radius: 6px;
        padding: 9px 13px;
        margin-bottom: 16px;
    }}
    .tax-box p {{
        margin: 0;
        font-size: 8pt;
        color: #166534;
        line-height: 1.45;
    }}
    .signature-area {{
        margin-top: 18px;
        width: 280px;
        page-break-inside: avoid;
    }}
    .signature-img {{
        display: block;
        max-height: 44px;
        max-width: 170px;
        margin-bottom: -5px;
        object-fit: contain;
    }}
    .signature-rule {{
        border-top: 1px solid #94a3b8;
        margin-bottom: 5px;
        width: 100%;
    }}
    .signature-name {{
        font-weight: 800;
        font-size: 10.5pt;
        color: #0f2b5c;
        letter-spacing: 0.3px;
        line-height: 1.25;
    }}
    .signature-meta {{
        font-size: 8.5pt;
        color: #475569;
        line-height: 1.35;
    }}
    .signature-email {{
        color: #2563eb;
    }}
</style>
</head>
<body>
    <div class="header-banner">
        <div class="header-title">CUENTA DE COBRO N° {html.escape(datos.num_cuenta)}</div>
        <div class="header-subtitle">Contrato de Prestación de Servicios Nº {html.escape(datos.num_contrato)}</div>
    </div>

    <table class="meta-grid">
        <tr>
            <td width="34%">
                <div class="meta-card">
                    <div class="meta-label">DEBE A (CONTRATISTA)</div>
                    <div class="meta-value">{html.escape(datos.emisor)}</div>
                    <div class="meta-sub">C.C. / NIT: {html.escape(datos.rut_emisor)}</div>
                    <div class="meta-sub">No responsable de IVA</div>
                </div>
            </td>
            <td width="33%">
                <div class="meta-card">
                    <div class="meta-label">A FAVOR DE (CONTRATANTE)</div>
                    <div class="meta-value">{html.escape(datos.cliente)}</div>
                    <div class="meta-sub">NIT: {html.escape(datos.nit_cliente)}</div>
                    <div class="meta-sub">{html.escape(datos.ciudad_cliente)}</div>
                </div>
            </td>
            <td width="33%">
                <div class="meta-card">
                    <div class="meta-label">FECHA DE EXPEDICIÓN</div>
                    <div class="meta-value">{html.escape(fecha_expedicion)}</div>
                    <div class="meta-sub">Período: {html.escape(datos.periodo_ejecucion)}</div>
                </div>
            </td>
        </tr>
    </table>

    <div class="section-title">1. CONCEPTO DEL COBRO</div>
    <div class="concept-box">
        {concepto_html}
    </div>

    <div class="section-title">2. LIQUIDACIÓN DEL SERVICIO</div>
    <table class="pricing-table">
        <thead>
            <tr>
                <th width="7%" class="text-center">ÍTEM</th>
                <th width="47%">DESCRIPCIÓN</th>
                <th width="12%" class="text-center">CANTIDAD</th>
                <th width="17%" class="text-right">VALOR UNITARIO</th>
                <th width="17%" class="text-right">VALOR TOTAL</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
            {filas_liquidacion_html}
        </tbody>
    </table>
    <div class="valor-letras-bar">
        <strong>VALOR EN LETRAS:</strong> <span>{html.escape(datos.total_en_letras)}</span>
    </div>

    <div class="section-title">3. DATOS PARA TRANSFERENCIA BANCARIA</div>
    <div class="bank-box">
        <table class="bank-table">
            <tr>
                <td class="lbl">Titular de la Cuenta:</td>
                <td class="val">{html.escape(datos.titular_cuenta)}</td>
            </tr>
            <tr>
                <td class="lbl">Identificación / NIT:</td>
                <td class="val">C.C. {html.escape(datos.rut_emisor)}</td>
            </tr>
            <tr>
                <td class="lbl">Entidad Bancaria:</td>
                <td class="val bold">{html.escape(datos.banco)}</td>
            </tr>
            <tr>
                <td class="lbl">Tipo de Cuenta:</td>
                <td class="val">{html.escape(datos.tipo_cuenta)}</td>
            </tr>
            <tr>
                <td class="lbl">Número de Cuenta:</td>
                <td class="val bold">{html.escape(datos.numero_cuenta)}</td>
            </tr>
        </table>
    </div>

    {seccion_tributaria_html}

    {bloque_firma_html}
</body>
</html>"""
