"""
Gestor de persistencia y configuración de la aplicación.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

import json
import os
import tempfile
from typing import Dict, Any

DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json"
)

DEFAULTS: Dict[str, Any] = {
    "cliente_defecto": "I.E. Técnica de Pasacaballos",
    "nit_cliente": "800.255.974-5",
    "ciudad_cliente": "Cartagena de Indias, D.T. y C.",
    "emisor": "Owen Badel Hooker",
    "rut": "1.047.503.800",
    "lugar_expedicion": "de Cartagena",
    "telefono": "3016450065",
    "email": "owenbadel19@gmail.com",
    "cargo": "Contratista de Servicios TI",
    "ciudad": "Cartagena / Pasacaballos",
    "consecutivo_cuenta": "001",
    "num_contrato": "15 del 31-08-2026",
    "periodo_ejecucion": "31-08-2026 a 07-09-2026",
    "periodo_largo": "31 de agosto al 07 de septiembre de 2026",
    "objeto_contrato": "Mantenimiento preventivo de computadores de mesa y/o portátiles, soporte técnico y configuración de impresoras.",
    "banco": "Bancolombia",
    "tipo_cuenta": "Ahorros",
    "numero_cuenta": "67800017891",
    "titular": "Owen Badel Hooker",
    "incluir_tributario": True,
    "incluir_firma": True,
    "texto_tributario": (
        "Manifiesto bajo la gravedad del juramento que pertenezco al régimen de "
        "No Responsables del Impuesto sobre las Ventas (IVA) de conformidad con el "
        "artículo 437 del Estatuto Tributario, por lo cual este documento soporte no causa dicho impuesto."
    )
}


def cargar_configuracion(ruta: str = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """Carga la configuración desde disco preservando defaults ante claves faltantes."""
    config = dict(DEFAULTS)
    if os.path.exists(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
                config.update(data)
        except Exception as e:
            print(f"[WARN] Error al leer {ruta}, usando defaults: {e}")
    return config


def guardar_configuracion(config_dict: Dict[str, Any], ruta: str = DEFAULT_CONFIG_PATH) -> bool:
    """Guarda la configuración en disco mediante escritura atómica para evitar corrupción."""
    dir_name = os.path.dirname(os.path.abspath(ruta))
    os.makedirs(dir_name, exist_ok=True)
    try:
        with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as tf:
            json.dump(config_dict, tf, ensure_ascii=False, indent=4)
            temp_name = tf.name
        # Reemplazo atómico en Windows / Linux
        os.replace(temp_name, ruta)
        return True
    except Exception as e:
        print(f"[ERROR] Error al guardar configuración en {ruta}: {e}")
        return False
