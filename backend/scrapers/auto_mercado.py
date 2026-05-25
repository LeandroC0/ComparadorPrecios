from playwright.sync_api import Page
from .base_scraper import BaseScraper


class AutoMercadoScraper(BaseScraper):

    @property
    def supermercado_id(self) -> str:
        return "auto_mercado"

    @property
    def base_url(self) -> str:
        return "https://automercado.cr/buscar?q=arroz"

    def scrape_productos(self, page: Page) -> list[dict]:
        productos = []

        try:
            print("[auto_mercado] Esperando carga completa...")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(5000)

            # Captura para debug
            page.screenshot(path="debug.png")

            print("[auto_mercado] Buscando productos...")

            # Buscar artículos/productos
            items = page.query_selector_all("article")

            print(f"[auto_mercado] {len(items)} items encontrados en pagina")

            for item in items:
                try:
                    texto = item.inner_text().strip()

                    # Ignorar vacíos
                    if not texto or len(texto) < 5:
                        continue

                    # Obtener URL
                    link_el = item.query_selector("a")
                    url = None

                    if link_el:
                        url = link_el.get_attribute("href")

                        if url and not url.startswith("http"):
                            url = "https://www.automercado.cr" + url

                    # Nombre del producto
                    nombre = texto.split("\n")[0].strip()

                    # Buscar precio
                    precio = None

                    for palabra in texto.split():
                        if "₡" in palabra:
                            precio = self._parsear_precio(palabra)
                            break

                    # Guardar producto
                    if nombre and precio:
                        productos.append({
                            "nombre": nombre,
                            "precio": precio,
                            "precio_por_unidad": None,
                            "unidad": None,
                            "url": url,
                        })

                        print(f"Producto encontrado: {nombre} - {precio}")

                except Exception as e:
                    print(f"[auto_mercado] Error parseando item: {e}")
                    continue

        except Exception as e:
            print(f"[auto_mercado] Error general: {e}")

        return productos

    def _parsear_precio(self, texto: str) -> float | None:
        """
        Convierte:
        ₡1.234,56 -> 1234.56
        ₡2.500 -> 2500
        """

        if not texto:
            return None

        try:
            limpio = (
                texto.replace("₡", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )

            return float(limpio)

        except ValueError:
            return None