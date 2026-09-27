"""
Utilidades auxiliares de sanitización, consecución y codificación de imágenes.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

import os
import re
import base64


def sanitizar_nombre_archivo(texto: str) -> str:
    """Elimina caracteres inválidos para nombres de archivo en Windows/Linux."""
    texto = re.sub(r'[\\/*?:"<>|]', "", texto)
    return texto.strip().replace(" ", "_")


def incrementar_consecutivo(consecutivo: str) -> str:
    """
    Incrementa de forma inteligente el sufijo numérico de un consecutivo preservando ceros a la izquierda.
    Ej: "001" -> "002", "CC-099" -> "CC-100"
    """
    consecutivo = str(consecutivo).strip()
    match = re.search(r'(\d+)$', consecutivo)
    if match:
        num_str = match.group(1)
        longitud = len(num_str)
        nuevo_num = int(num_str) + 1
        nuevo_num_str = str(nuevo_num).zfill(longitud)
        return consecutivo[:match.start(1)] + nuevo_num_str
    return consecutivo


def obtener_imagen_base64(ruta_imagen: str) -> str:
    """Codifica una imagen local a Data URI Base64 para incrustación directa en HTML."""
    if ruta_imagen and os.path.exists(ruta_imagen):
        try:
            with open(ruta_imagen, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                ext = os.path.splitext(ruta_imagen)[1].lower().replace(".", "")
                mime = "image/png" if ext == "png" else ("image/jpeg" if ext in ("jpg", "jpeg") else "image/png")
                return f"data:{mime};base64,{b64}"
        except Exception as e:
            print(f"[WARN] No se pudo codificar la imagen {ruta_imagen}: {e}")
            return ""
    return ""
