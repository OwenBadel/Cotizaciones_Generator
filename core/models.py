"""
Modelos de datos fuertemente tipados para Cotizaciones y Cuentas de Cobro.
Soporta liquidaciones comerciales avanzadas (descuentos, IVA opcional y retenciones en la fuente/ICA).
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

from dataclasses import dataclass, field
from typing import List, Optional
from .currency import formato_moneda_colombiana, formato_moneda_letras


@dataclass
class ItemCotizacion:
    """Representa un renglón o ítem de cobro/cotización."""
    descripcion: str
    cantidad: int = 1
    precio_unitario: float = 0.0

    @property
    def total(self) -> float:
        """Calcula el valor total del ítem."""
        return round(self.cantidad * self.precio_unitario, 2)

    @property
    def precio_unitario_formateado(self) -> str:
        """Retorna el precio unitario en formato moneda colombiana."""
        return formato_moneda_colombiana(self.precio_unitario)

    @property
    def total_formateado(self) -> str:
        """Retorna el total del ítem en formato moneda colombiana."""
        return formato_moneda_colombiana(self.total)


@dataclass
class DatosCotizacion:
    """Datos consolidados para generar una Cotización o Propuesta de Servicios."""
    cliente: str
    emisor: str
    rut_emisor: str
    fecha: str
    consecutivo: str = "COT-001"
    forma_pago: str = "50% anticipo y 50% al finalizar"
    vigencia_dias: int = 15
    objetivo_servicio: str = ""
    detalle_servicios: str = ""
    descuento_porcentaje: float = 0.0
    aplicar_iva: bool = False
    iva_porcentaje: float = 19.0
    items: List[ItemCotizacion] = field(default_factory=list)

    @property
    def subtotal(self) -> float:
        """Suma bruta de los ítems cotizados."""
        return round(sum(item.total for item in self.items), 2)

    @property
    def subtotal_formateado(self) -> str:
        return formato_moneda_colombiana(self.subtotal)

    @property
    def descuento_valor(self) -> float:
        """Valor deducido por descuento comercial."""
        if self.descuento_porcentaje <= 0.0:
            return 0.0
        return round(self.subtotal * (self.descuento_porcentaje / 100.0), 2)

    @property
    def descuento_formateado(self) -> str:
        return formato_moneda_colombiana(self.descuento_valor)

    @property
    def base_imponible(self) -> float:
        return round(self.subtotal - self.descuento_valor, 2)

    @property
    def iva_valor(self) -> float:
        """Valor del IVA si aplica a la propuesta."""
        if not self.aplicar_iva:
            return 0.0
        return round(self.base_imponible * (self.iva_porcentaje / 100.0), 2)

    @property
    def iva_formateado(self) -> str:
        return formato_moneda_colombiana(self.iva_valor)

    @property
    def total_general(self) -> float:
        """Monto neto liquidado."""
        return round(self.base_imponible + self.iva_valor, 2)

    @property
    def total_formateado(self) -> str:
        return formato_moneda_colombiana(self.total_general)

    @property
    def total_en_letras(self) -> str:
        return formato_moneda_letras(self.total_general)


@dataclass
class DatosCuentaCobro:
    """Datos consolidados para generar una Cuenta de Cobro oficial de servicios."""
    num_cuenta: str
    num_contrato: str
    periodo_ejecucion: str
    periodo_largo: str
    objeto_contrato: str
    concepto_cobro: str
    cliente: str
    nit_cliente: str
    ciudad_cliente: str
    emisor: str
    rut_emisor: str
    lugar_expedicion: str
    telefono: str
    email: str
    cargo: str
    banco: str
    tipo_cuenta: str
    numero_cuenta: str
    titular_cuenta: str
    incluir_tributario: bool = True
    incluir_firma: bool = True
    aplicar_retefuente: bool = False
    retefuente_porcentaje: float = 4.0
    aplicar_reteica: bool = False
    reteica_porcentaje: float = 0.966
    texto_tributario: str = (
        "Manifiesto bajo la gravedad del juramento que pertenezco al régimen de "
        "No Responsables del Impuesto sobre las Ventas (IVA) de conformidad con el "
        "artículo 437 del Estatuto Tributario, por lo cual este documento soporte no causa dicho impuesto."
    )
    ruta_firma: Optional[str] = None
    items: List[ItemCotizacion] = field(default_factory=list)

    @property
    def subtotal_bruto(self) -> float:
        """Suma de los ítems de cobro antes de retenciones."""
        return round(sum(item.total for item in self.items), 2)

    @property
    def subtotal_bruto_formateado(self) -> str:
        return formato_moneda_colombiana(self.subtotal_bruto)

    @property
    def retefuente_valor(self) -> float:
        if not self.aplicar_retefuente:
            return 0.0
        return round(self.subtotal_bruto * (self.retefuente_porcentaje / 100.0), 2)

    @property
    def retefuente_formateado(self) -> str:
        return formato_moneda_colombiana(self.retefuente_valor)

    @property
    def reteica_valor(self) -> float:
        if not self.aplicar_reteica:
            return 0.0
        return round(self.subtotal_bruto * (self.reteica_porcentaje / 100.0), 2)

    @property
    def reteica_formateado(self) -> str:
        return formato_moneda_colombiana(self.reteica_valor)

    @property
    def total_deducciones(self) -> float:
        return round(self.retefuente_valor + self.reteica_valor, 2)

    @property
    def total_general(self) -> float:
        """Neto a pagar luego de retenciones tributarias."""
        return round(self.subtotal_bruto - self.total_deducciones, 2)

    @property
    def total_formateado(self) -> str:
        return formato_moneda_colombiana(self.total_general)

    @property
    def total_en_letras(self) -> str:
        return formato_moneda_letras(self.total_general)
