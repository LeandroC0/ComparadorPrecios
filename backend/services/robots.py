import random
import ssl
import time
import urllib.request
import urllib.robotparser
from functools import lru_cache


# =========================================================
# USER AGENTS
# =========================================================

USER_AGENTS = [
    # Chrome Windows
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),

    # Firefox Windows
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) "
        "Gecko/20100101 Firefox/139.0"
    ),

    # Edge Windows
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
    ),
]


# =========================================================
# SUPERMERCADOS
# =========================================================

SUPERMERCADOS = {
    "walmart": "https://www.walmart.co.cr",
    "maxi_pali": "https://www.maxipali.co.cr",
    "auto_mercado": "https://www.automercado.cr",
    "pricesmart": "https://www.pricesmart.com",
    "megasuper": "https://www.megasuper.net",
    "mayca": "https://www.mayca.com",
}


# =========================================================
# SSL
# =========================================================

_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE


# =========================================================
# HELPERS
# =========================================================

def obtener_user_agent():
    return random.choice(USER_AGENTS)


def generar_headers():
    return {
        "User-Agent": obtener_user_agent(),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "es-CR,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
    }


def delay_humano(min_seg=2, max_seg=6):
    tiempo = random.uniform(min_seg, max_seg)
    print(f"[delay] Esperando {tiempo:.2f}s")
    time.sleep(tiempo)


# =========================================================
# ROBOTS.TXT
# =========================================================

def _leer_robots_txt(base_url: str) -> str:
    url = f"{base_url}/robots.txt"

    try:
        req = urllib.request.Request(
            url,
            headers=generar_headers()
        )

        with urllib.request.urlopen(
            req,
            context=_ssl_ctx,
            timeout=10
        ) as resp:

            return resp.read().decode("utf-8", errors="ignore")

    except Exception as e:
        print(f"[robots] Error leyendo robots.txt: {e}")
        return ""


@lru_cache(maxsize=10)
def _cargar_robots(base_url: str):

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{base_url}/robots.txt")

    contenido = _leer_robots_txt(base_url)

    if contenido:
        rp.parse(contenido.splitlines())

    return rp


def can_fetch(supermercado_id: str, path: str = "/") -> bool:

    base_url = SUPERMERCADOS.get(supermercado_id)

    if not base_url:
        print(f"[robots] Supermercado desconocido")
        return False

    rp = _cargar_robots(base_url)

    url_completa = f"{base_url}{path}"

    permitido = rp.can_fetch(
        obtener_user_agent(),
        url_completa
    )

    if not permitido:
        print(f"[robots] Acceso denegado: {path}")

    return permitido


# =========================================================
# REQUESTS
# =========================================================

def hacer_request(url: str):

    delay_humano()

    headers = generar_headers()

    print(f"[request] URL: {url}")
    print(f"[request] UA: {headers['User-Agent']}")

    req = urllib.request.Request(
        url,
        headers=headers
    )

    with urllib.request.urlopen(
        req,
        context=_ssl_ctx,
        timeout=15
    ) as response:

        html = response.read().decode(
            "utf-8",
            errors="ignore"
        )

        return html


# =========================================================
# DEBUG
# =========================================================

def ver_robots(supermercado_id: str):

    base_url = SUPERMERCADOS.get(supermercado_id)

    if not base_url:
        print("Supermercado inválido")
        return

    print(_leer_robots_txt(base_url))


def limpiar_cache():
    _cargar_robots.cache_clear()


# =========================================================
# EJEMPLO
# =========================================================

if __name__ == "__main__":

    permitido = can_fetch(
        "walmart",
        "/"
    )

    print(f"Permitido: {permitido}")

    if permitido:

        html = hacer_request(
            "https://www.walmart.co.cr"
        )

        print(html[:500])