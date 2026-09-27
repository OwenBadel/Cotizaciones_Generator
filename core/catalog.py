"""
Catálogo de servicios y productos tecnológicos frecuentes para inserción rápida.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ServicioCatalogo:
    """Definición de un servicio o producto estandarizado del catálogo."""
    categoria: str
    descripcion: str
    precio_sugerido: float
    cantidad_defecto: int = 1


CATALOGO_SERVICIOS_TI: List[ServicioCatalogo] = [
    ServicioCatalogo(
        categoria="Mantenimiento y Soporte",
        descripcion="Mantenimiento preventivo integral de computador (limpieza interna, cambio de pasta térmica, optimización de SO)",
        precio_sugerido=75000.0,
        cantidad_defecto=1
    ),
    ServicioCatalogo(
        categoria="Mantenimiento y Soporte",
        descripcion="Mantenimiento preventivo y correctivo básico de impresora multifuncional (limpieza de rodillos, lubricación y calibración)",
        precio_sugerido=65000.0,
        cantidad_defecto=1
    ),
    ServicioCatalogo(
        categoria="Mantenimiento y Soporte",
        descripcion="Póliza mensual de soporte técnico preventivo y correctivo por equipo de cómputo",
        precio_sugerido=50000.0,
        cantidad_defecto=10
    ),
    ServicioCatalogo(
        categoria="Redes e Infraestructura",
        descripcion="Instalación y configuración de Switch Gigabit administrable (segmentación VLANs y optimización de tráfico)",
        precio_sugerido=280000.0,
        cantidad_defecto=1
    ),
    ServicioCatalogo(
        categoria="Redes e Infraestructura",
        descripcion="Configuración de Router / Puntos de Acceso Wi-Fi 6 Mesh con aislamiento de red para invitados",
        precio_sugerido=160000.0,
        cantidad_defecto=1
    ),
    ServicioCatalogo(
        categoria="Redes e Infraestructura",
        descripcion="Tendido, ponchado, rotulado y certificación de punto de red estructurada Cat 6/6A",
        precio_sugerido=45000.0,
        cantidad_defecto=4
    ),
    ServicioCatalogo(
        categoria="Seguridad y Software",
        descripcion="Auditoría de ciberseguridad perimetral, configuración de Firewall y políticas de respaldo automatizado (Backup 3-2-1)",
        precio_sugerido=550000.0,
        cantidad_defecto=1
    ),
    ServicioCatalogo(
        categoria="Seguridad y Software",
        descripcion="Desarrollo de software a medida, automatización agéntica o integración API REST (Tarifa por Hora de Ingeniería)",
        precio_sugerido=95000.0,
        cantidad_defecto=10
    ),
]
