import re


def detectar_bloqueo(html: str) -> bool:
    """
    Detecta posibles páginas de bloqueo.
    """

    if not html:
        return True

    html = html.lower()

    patrones = [

        r"captcha",

        r"access denied",

        r"temporarily blocked",

        r"verify you are human",

        r"robot or human",

        r"cloudflare",

        r"challenge-platform",

        r"forbidden",

        r"security check",

        r"unusual traffic",
    ]

    return any(
        re.search(p, html)
        for p in patrones
    )