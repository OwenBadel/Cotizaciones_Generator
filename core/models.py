"""
Modelos de datos fuertemente tipados para Cotizaciones y Cuentas de Cobro.
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
    forma_pago: str = "50% anticipo y 50% al finalizar"
    objetivo_servicio: str = ""
    detalle_servicios: str = ""
    items: List[ItemCotizacion] = field(default_factory=list)

    @property
    def total_general(self) -> float:
        """Suma de todos los ítems."""
        return round(sum(item.total for item in self.items), 2)

    @property
    def total_formateado(self) -> str:
        """Total general formateado en pesos colombianos."""
        return formato_moneda_colombiana(self.total_general)

    @property
    def total_en_letras(self) -> str:
        """Total general expresado en letras (formato oficial)."""
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
    texto_tributario: str = (
        "Manifiesto bajo la gravedad del juramento que pertenezco al régimen de "
        "No Responsables del Impuesto sobre las Ventas (IVA) de conformidad con el "
        "artículo 437 del Estatuto Tributario, por lo cual este documento soporte no causa dicho impuesto."
    )
    ruta_firma: Optional[str] = None
    items: List[ItemCotizacion] = field(default_factory=list)

    @property
    def total_general(self) -> float:
        """Suma total de los ítems de cobro."""
        return round(sum(item.total for item in self.items), 2)

    @property
    def total_formateado(self) -> str:
        """Total general formateado en pesos colombianos."""
        return formato_moneda_colombiana(self.total_general)

    @property
    def total_en_letras(self) -> str:
        """Total general en letras conforme a la normativa colombiana."""
        return formato_moneda_letras(self.total_general)
