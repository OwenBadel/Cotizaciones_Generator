"""
Plantilla HTML/CSS de alta fidelidad para Cotización / Propuesta Técnica TI.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

import html
from core.models import DatosCotizacion


def render_cotizacion_html(datos: DatosCotizacion) -> str:
    """Renderiza el documento HTML/CSS imprimible para la Cotización/Propuesta."""
    num_seccion = 1

    seccion_objetivo_html = ""
    if datos.objetivo_servicio.strip():
        texto_sani = html.escape(datos.objetivo_servicio.strip())
        seccion_objetivo_html = f"""
        <div class="block-group">
            <h2>{num_seccion}. Objetivo del Servicio</h2>
            <div class="section-card"><p>{texto_sani}</p></div>
        </div>
        """
        num_seccion += 1

    seccion_detalle_html = ""
    if datos.detalle_servicios.strip():
        lineas = datos.detalle_servicios.strip().split('\n')
        items_li = "".join([
            f"<li style='margin-bottom: 6px;'>{html.escape(linea.replace('•', '').strip())}</li>"
            for linea in lineas if linea.strip()
        ])
        seccion_detalle_html = f"""
        <div class="block-group">
            <h2>{num_seccion}. Detalle de los Servicios y Productos</h2>
            <div class="section-card">
                <ul style="margin: 0; padding-left: 18px; color: #334155;">
                    {items_li}
                </ul>
            </div>
        </div>
        """
        num_seccion += 1

    seccion_cotizacion_num = num_seccion
    num_seccion += 1

    seccion_pago_html = ""
    if datos.forma_pago == "50% anticipo y 50% al finalizar":
        seccion_pago_html = f"""
        <div class="block-group">
            <h2>{num_seccion}. Términos y Condiciones</h2>
            <div class="terms-box">
                <p><strong>Forma de Pago:</strong> 50% de anticipo al momento de la firma/aprobación de la propuesta (para la compra de insumos y equipos de red) y 50% restante al finalizar las actividades.</p>
            </div>
        </div>
        """
        num_seccion += 1
    elif datos.forma_pago == "Pago contra entrega (100%)":
        seccion_pago_html = f"""
        <div class="block-group">
            <h2>{num_seccion}. Términos y Condiciones</h2>
            <div class="terms-box">
                <p><strong>Forma de Pago:</strong> 100% contra entrega a entera satisfacción del cliente una vez finalizadas las actividades y entregados los servicios/equipos.</p>
            </div>
        </div>
        """
        num_seccion += 1

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

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
    @page {{
        size: A4;
        margin: 18mm 16mm;
    }}
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1e293b;
        margin: 0;
        padding: 0;
        font-size: 10pt;
        line-height: 1.5;
        background-color: #ffffff;
    }}
    .block-group {{
        page-break-inside: avoid;
        margin-bottom: 16px;
    }}
    .block-group.flow {{ page-break-inside: auto; }}
    .header-banner {{
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        color: #ffffff;
        padding: 22px 26px;
        border-radius: 12px;
        margin-bottom: 20px;
    }}
    .header-title {{ font-size: 17pt; font-weight: 700; letter-spacing: 0.5px; margin: 0 0 4px 0; color: #ffffff; text-transform: uppercase; }}
    .header-subtitle {{ font-size: 10.5pt; color: #93c5fd; font-weight: 500; margin: 0; }}
    .meta-grid {{ width: 100%; margin-bottom: 20px; border-collapse: separate; border-spacing: 10px 0; }}
    .meta-card {{ background-color: #f8fafc; padding: 10px 14px; border-radius: 8px; border-left: 4px solid #2563eb; border-top: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; }}
    .meta-label {{ font-size: 8pt; text-transform: uppercase; color: #64748b; font-weight: 700; margin-bottom: 2px; }}
    .meta-value {{ font-size: 9.5pt; color: #0f172a; font-weight: 600; }}
    h2 {{ font-size: 11pt; color: #1e3a8a; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 15px; margin-bottom: 10px; padding-bottom: 4px; border-bottom: 2px solid #e2e8f0; }}
    p {{ margin: 0 0 8px 0; color: #334155; }}
    .section-card {{ background: #ffffff; padding: 14px; border-radius: 8px; border: 1px solid #e2e8f0; }}
    table.pricing-table {{ width: 100%; border-collapse: collapse; margin-top: 8px; margin-bottom: 16px; background: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e2e8f0; page-break-inside: auto; }}
    table.pricing-table thead {{ display: table-header-group; }}
    table.pricing-table tr {{ page-break-inside: avoid; }}
    table.pricing-table th {{ background-color: #1e293b; color: #ffffff; font-weight: 600; text-align: left; padding: 9px 11px; font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.5px; }}
    table.pricing-table td {{ padding: 9px 11px; border-bottom: 1px solid #f1f5f9; color: #334155; font-size: 9pt; word-wrap: break-word; overflow-wrap: break-word; }}
    table.pricing-table tr:nth-child(even) td {{ background-color: #f8fafc; }}
    .text-center {{ text-align: center; }}
    .text-right {{ text-align: right; }}
    .total-row td {{ background-color: #eff6ff !important; font-weight: 700; color: #1e3a8a; font-size: 10.5pt; border-top: 2px solid #2563eb; }}
    .terms-box {{ background-color: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; padding: 12px 14px; border-radius: 8px; page-break-inside: avoid; }}
    .terms-box p {{ color: #166534; margin: 0; font-weight: 500; }}
    .footer-signature {{ margin-top: 30px; padding-top: 12px; border-top: 1px solid #cbd5e1; width: 220px; page-break-inside: avoid; }}
    .signature-line {{ font-weight: 700; color: #0f172a; line-height: 1.3; }}
    .signature-title {{ font-size: 8.5pt; color: #64748b; line-height: 1.3; }}
</style>
</head>
<body>
    <div class="block-group">
        <div class="header-banner">
            <div class="header-title">Propuesta Técnica SERVICIOS TI</div>
            <div class="header-subtitle">Servicios Tecnológicos de Infraestructura y Redes</div>
        </div>
        <table class="meta-grid">
            <tr>
                <td width="33%"><div class="meta-card"><div class="meta-label">Cliente</div><div class="meta-value">{html.escape(datos.cliente)}</div></div></td>
                <td width="33%"><div class="meta-card"><div class="meta-label">Preparado Por</div><div class="meta-value">{html.escape(datos.emisor)}</div><div style="font-size: 7.5pt; color: #64748b;">NIT/RUT: {html.escape(datos.rut_emisor)}</div></div></td>
                <td width="34%"><div class="meta-card"><div class="meta-label">Fecha de Emisión</div><div class="meta-value">{html.escape(datos.fecha)}</div></div></td>
            </tr>
        </table>
    </div>

    {seccion_objetivo_html}

    {seccion_detalle_html}
    <div class="block-group flow">
        <h2>{seccion_cotizacion_num}. Cotización</h2>
        <table class="pricing-table">
            <thead>
                <tr>
                    <th width="8%" class="text-center">Ítem</th>
                    <th width="48%">Descripción</th>
                    <th width="12%" class="text-center">Cantidad</th>
                    <th width="16%" class="text-right">Valor Unitario</th>
                    <th width="16%" class="text-right">Valor Total</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
                <tr class="total-row">
                    <td colspan="3" class="text-right"><strong>TOTAL PROPUESTA</strong></td>
                    <td colspan="2" class="text-right"><strong>{datos.total_formateado} COP</strong></td>
                </tr>
            </tbody>
        </table>
    </div>

    {seccion_pago_html}

    <div class="footer-signature">
        <div class="signature-line">{html.escape(datos.emisor)}</div>
        <div class="signature-title">Servicios y Soluciones TI</div>
        <div class="signature-title">NIT / RUT: {html.escape(datos.rut_emisor)}</div>
    </div>
</body>
</html>"""
