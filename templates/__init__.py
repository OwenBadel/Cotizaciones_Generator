"""Módulo de plantillas HTML/CSS profesionales para cotizaciones y cuentas de cobro."""
from .cotizacion_template import render_cotizacion_html
from .cuenta_cobro_template import render_cuenta_cobro_html

__all__ = ["render_cotizacion_html", "render_cuenta_cobro_html"]
