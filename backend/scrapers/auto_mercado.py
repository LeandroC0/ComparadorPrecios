from playwright.sync_api import Page

from .base_scraper import BaseScraper


class AutoMercadoScraper(
    BaseScraper
):

    @property
    def supermercado_id(self) -> str:

        return "auto_mercado"

    @property
    def base_url(self) -> str:

        return (
            "https://www.automercado.cr/"
            "buscar?q=arroz"
        )

    def scrape_productos(
        self,
        page: Page
    ) -> list[dict]:

        productos = []

        try:

            page.wait_for_selector(

                ".card.card-product",

                timeout=15000
            )

            self.delay()

            items = page.query_selector_all(
                ".card.card-product"
            )

            print(
                f"[auto_mercado] "
                f"{len(items)} cards encontradas"
            )

            # Delay entre productos
            for item in items:

                self.delay()

                try:

                    nombre_el = item.query_selector(
                        ".title-product span"
                    )

                    nombre = (
                        nombre_el.inner_text().strip()
                        if nombre_el else None
                    )

                    precio_el = item.query_selector(
                        ".text-currency"
                    )

                    precio_texto = (
                        precio_el.inner_text().strip()
                        if precio_el else None
                    )

                    precio = self._parsear_precio(
                        precio_texto
                    )

                    precio_original_el = (
                        item.query_selector(
                            ".discount-price span"
                        )
                    )

                    precio_original_texto = (

                        precio_original_el
                        .inner_text()
                        .strip()

                        if precio_original_el
                        else None
                    )

                    precio_original = (
                        self._parsear_precio(
                            precio_original_texto
                        )
                    )

                    tag_el = item.query_selector(
                        ".product-tag span:last-child"
                    )

                    tag_texto = (
                        tag_el.inner_text().strip()
                        if tag_el else ""
                    )

                    es_promo = (
                        "%" in tag_texto
                    )

                    link_el = item.query_selector(
                        "a.img-product"
                    )

                    url = (
                        link_el.get_attribute("href")
                        if link_el else None
                    )

                    if (
                        url
                        and not url.startswith("http")
                    ):

                        url = (
                            "https://www.automercado.cr"
                            + url
                        )

                    img_el = item.query_selector(
                        "a.img-product img"
                    )

                    imagen_url = (
                        img_el.get_attribute("src")
                        if img_el else None
                    )

                    # Limpia espacios
                    if imagen_url:

                        imagen_url = (
                            imagen_url
                            .strip()
                            .replace(" ", "")
                        )

                    subtitulo_el = item.query_selector(
                        ".text-subtitle span"
                    )

                    subtitulo = (
                        subtitulo_el.inner_text().strip()
                        if subtitulo_el else ""
                    )

                    precio_por_unidad, unidad = (
                        self._calcular_precio_unidad(
                            precio,
                            subtitulo
                        )
                    )

                    if nombre and precio:

                        productos.append({

                            "nombre":
                                nombre,

                            "precio":
                                precio,

                            "precio_original":
                                precio_original,

                            "precio_por_unidad":
                                precio_por_unidad,

                            "unidad":
                                unidad,

                            "es_promo":
                                es_promo,

                            "imagen_url":
                                imagen_url,

                            "url":
                                url,
                        })

                except Exception as e:

                    print(
                        f"[auto_mercado] "
                        f"Error parseando: {e}"
                    )

                    continue

        except Exception as e:

            print(
                f"[auto_mercado] Error: {e}"
            )

        return productos

    def _parsear_precio(
        self,
        texto: str
    ) -> float | None:

        if not texto:
            return None

        try:

            limpio = (
                texto
                .replace("₡", "")
                .replace(",", "")
                .strip()
            )

            return float(limpio)

        except ValueError:

            return None

    def _calcular_precio_unidad(
        self,
        precio: float,
        subtitulo: str
    ) -> tuple:

        if not precio or not subtitulo:
            return None, None

        import re

        match = re.search(

            r"(\d+(?:\.\d+)?)\s*(g|kg|ml|l)\b",

            subtitulo.lower()
        )

        if not match:
            return None, None

        cantidad = float(
            match.group(1)
        )

        unidad = match.group(2)

        if unidad == "kg":

            cantidad *= 1000
            unidad = "g"

        elif unidad == "l":

            cantidad *= 1000
            unidad = "ml"

        return (
            round(precio / cantidad, 4),
            unidad
        )