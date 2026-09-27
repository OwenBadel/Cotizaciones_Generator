"""
Módulo de formateo monetario y conversión de números a letras para pesos colombianos.
Autor: Owen Badel Hooker — Ingeniero de Sistemas
"""

import re
from typing import Union


def numero_a_letras(numero: Union[int, float]) -> str:
    """
    Convierte una cifra numérica a su representación literal en español.
    Maneja unidades, decenas, centenas, miles y millones.
    """
    numero = int(round(numero))
    if numero == 0:
        return "CERO"

    unidades = ["", "UN", "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE"]
    especiales = {
        10: "DIEZ", 11: "ONCE", 12: "DOCE", 13: "TRECE", 14: "CATORCE", 15: "QUINCE",
        16: "DIECISEIS", 17: "DIECISIETE", 18: "DIECIOCHO", 19: "DIECINUEVE",
        20: "VEINTE", 21: "VEINTIUN", 22: "VEINTIDOS", 23: "VEINTITRES", 24: "VEINTICUATRO",
        25: "VEINTICINCO", 26: "VEINTISEIS", 27: "VEINTISIETE", 28: "VEINTIOCHO", 29: "VEINTINUEVE"
    }
    decenas = ["", "DIEZ", "VEINTE", "TREINTA", "CUARENTA", "CINCUENTA", "SESENTA", "SETENTA", "OCHENTA", "NOVENTA"]
    centenas = [
        "", "CIENTO", "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS",
        "QUINIENTOS", "SEISCIENTOS", "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS"
    ]

    def _seccion(n: int) -> str:
        if n == 0:
            return ""
        if n == 100:
            return "CIEN"

        c = n // 100
        resto = n % 100

        texto = centenas[c]
        if resto == 0:
            return texto

        if texto:
            texto += " "

        if resto in especiales:
            texto += especiales[resto]
        else:
            d = resto // 10
            u = resto % 10
            if d > 0:
                texto += decenas[d]
                if u > 0:
                    texto += " Y " + unidades[u]
            else:
                texto += unidades[u]
        return texto.strip()

    if numero < 1000:
        return _seccion(numero)

    partes = []

    millones = numero // 1000000
    resto = numero % 1000000
    if millones > 0:
        if millones == 1:
            partes.append("UN MILLÓN")
        else:
            partes.append(f"{numero_a_letras(millones)} MILLONES")

    miles = resto // 1000
    unidades_finales = resto % 1000
    if miles > 0:
        if miles == 1:
            partes.append("MIL")
        else:
            partes.append(f"{_seccion(miles)} MIL")

    if unidades_finales > 0:
        partes.append(_seccion(unidades_finales))

    return " ".join(partes)


def formato_moneda_letras(valor: float) -> str:
    """
    Retorna el valor literal estándar para facturación y cuentas de cobro en Colombia.
    Ej: "UN MILLÓN QUINIENTOS MIL PESOS M/CTE."
    """
    val_int = int(round(valor))
    letras = numero_a_letras(val_int)
    if val_int == 1:
        return f"{letras} PESO M/CTE."
    elif val_int % 1000000 == 0 and val_int > 0:
        return f"{letras} DE PESOS M/CTE."
    else:
        return f"{letras} PESOS M/CTE."


def formato_moneda_colombiana(valor: float, con_decimales: bool = True, con_cop: bool = False) -> str:
    """
    Formatea una cifra numérica al estándar monetario colombiano con puntos de miles y coma decimal.
    Ej: 1500000 -> "$1.500.000,00" o "$1.500.000"
    """
    if con_decimales:
        entero = int(valor)
        decimales = int(round((abs(valor) - abs(entero)) * 100))
        parte_entera = f"{entero:,}".replace(",", ".")
        res = f"${parte_entera},{decimales:02d}"
    else:
        parte_entera = f"{int(round(valor)):,}".replace(",", ".")
        res = f"${parte_entera}"
    if con_cop:
        res += " COP"
    return res


def parsear_valor_moneda(texto: str) -> float:
    """
    Convierte cadenas con símbolos de moneda, comas y puntos a float nativo.
    Ej: "$ 1.500.000,00" -> 1500000.0
    """
    texto = texto.replace("$", "").replace("COP", "").strip()
    if not texto:
        return 0.0
    if "," in texto:
        partes = texto.rsplit(",", 1)
        if len(partes[1].strip()) == 2 and partes[1].strip().isdigit():
            entero = re.sub(r'\D', '', partes[0])
            return float(f"{entero}.{partes[1].strip()}")
    if "." in texto:
        partes = texto.rsplit(".", 1)
        if len(partes[1].strip()) == 2 and partes[1].strip().isdigit():
            entero = re.sub(r'\D', '', partes[0])
            return float(f"{entero}.{partes[1].strip()}")
    limpio = re.sub(r'\D', '', texto)
    return float(limpio) if limpio else 0.0
