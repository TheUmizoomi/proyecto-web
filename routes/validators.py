import re
from datetime import datetime


def clean_text(value: str) -> str:
    return (value or "").strip()


def parse_int(value: str):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_float(value: str):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


NUMBERS_ONLY_RE = re.compile(r"^\d+$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def limpiar_texto(valor: str) -> str:
    return clean_text(valor)


def validar_solo_numeros(valor: str) -> bool:
    return bool(NUMBERS_ONLY_RE.fullmatch(clean_text(valor)))


def validar_solo_texto(valor: str) -> bool:
    texto = clean_text(valor)
    if not texto:
        return False
    # Permite letras (incluye acentos/ñ) y espacios. No permite números.
    return all((c.isalpha() or c.isspace()) for c in texto)


def validar_correo(valor: str) -> bool:
    return bool(EMAIL_RE.fullmatch(clean_text(valor).lower()))


def obtener_periodo_actual() -> str:
    mes = datetime.now().month
    if mes <= 6:
        return "ENERO-JUNIO"
    return "AGOSTO-DICIEMBRE"
