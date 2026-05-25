import os
import random
import time
from abc import ABC, abstractmethod
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser


class BaseScraper(ABC):

    def __init__(self):
        self.delay_min = float(os.environ.get("SCRAPING_DELAY_MIN", 2))
        self.delay_max = float(os.environ.get("SCRAPING_DELAY_MAX", 5))
        self.headless   = os.environ.get("HEADLESS", "true").lower() == "true"
        self.browser: Browser = None
        self.playwright = None

    # ------------------------------------------------------------------
    # Propiedades que cada scraper debe definir
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def supermercado_id(self) -> str:
        """Ej: 'walmart', 'auto_mercado'"""
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        """URL base del supermercado"""
        pass

    # ------------------------------------------------------------------
    # Metodo principal que cada scraper debe implementar
    # ------------------------------------------------------------------

    @abstractmethod
    def scrape_productos(self, page: Page) -> list[dict]:
        """
        Recibe una pagina de Playwright ya abierta.
        Debe retornar una lista de dicts con esta estructura:
        {
            "nombre": str,
            "precio": float,
            "precio_por_unidad": float | None,
            "unidad": str | None,
            "url": str,
        }
        """
        pass

    # ------------------------------------------------------------------
    # Metodos de utilidad disponibles para todos los scrapers
    # ------------------------------------------------------------------

    def delay(self):
        """Espera aleatoria entre requests para evitar bloqueos"""
        segundos = random.uniform(self.delay_min, self.delay_max)
        time.sleep(segundos)

    def iniciar_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        return self.browser

    def cerrar_browser(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def nueva_pagina(self):
        """Crea una pagina con headers que simulan un navegador real"""
        context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="es-CR",
        )
        return context.new_page()

    # ------------------------------------------------------------------
    # Metodo que orquesta todo el proceso
    # ------------------------------------------------------------------

    def ejecutar(self) -> list[dict]:
        """
        Abre el navegador, ejecuta el scraping y cierra todo.
        Retorna la lista de productos con timestamp y supermercado.
        """
        resultados = []
        try:
            self.iniciar_browser()
            page = self.nueva_pagina()

            print(f"[{self.supermercado_id}] Iniciando scraping en {self.base_url}")
            page.goto(self.base_url, wait_until="networkidle", timeout=60000)
            self.delay()

            productos = self.scrape_productos(page)

            for p in productos:
                p["supermercado"] = self.supermercado_id
                p["fecha_hora"]   = datetime.utcnow()

            resultados = productos
            print(f"[{self.supermercado_id}] {len(productos)} productos encontrados")

        except Exception as e:
            print(f"[{self.supermercado_id}] Error durante scraping: {e}")

        finally:
            self.cerrar_browser()

        return resultados