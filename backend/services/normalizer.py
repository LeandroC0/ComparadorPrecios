import re


def normalizar_nombre(nombre: str) -> str:
    """
    Normaliza nombres para evitar duplicados.
    """

    if not nombre:
        return ""

    nombre = nombre.lower()

    # Elimina caracteres especiales
    nombre = re.sub(
        r"[^a-z0-9áéíóúüñ ]",
        "",
        nombre
    )

    # Unifica unidades comunes
    reemplazos = {

        "litros": "l",
        "litro": "l",

        "kilogramos": "kg",
        "kilogramo": "kg",

        "gramos": "g",
        "gramo": "g",

        "mililitros": "ml",
        "mililitro": "ml",
    }

    for viejo, nuevo in reemplazos.items():
        nombre = nombre.replace(
            viejo,
            nuevo
        )

    # Elimina espacios múltiples
    nombre = re.sub(
        r"\s+",
        " ",
        nombre
    )

    return nombre.strip()