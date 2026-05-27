import os
import random
import time

from abc import ABC, abstractmethod
from datetime import datetime

from playwright.sync_api import (
    sync_playwright,
    Page,
    BrowserContext
)

from playwright_stealth import Stealth

from backend.services.robots import can_fetch
from backend.services.anti_bot import detectar_bloqueo
from backend.services.logger import logger


# User-Agents realistas
USER_AGENTS = [

    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),

    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) "
        "Gecko/20100101 Firefox/139.0"
    ),

    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
    ),
]


class BaseScraper(ABC):

    def __init__(self):

        # Delays configurables
        self.delay_min = float(
            os.environ.get(
                "SCRAPING_DELAY_MIN",
                4
            )
        )

        self.delay_max = float(
            os.environ.get(
                "SCRAPING_DELAY_MAX",
                10
            )
        )

        # Mostrar navegador
        self.headless = (
            os.environ.get(
                "HEADLESS",
                "false"
            ).lower() == "true"
        )

        # Cantidad máxima de reintentos
        self.max_retries = 3

        self.playwright = None
        self.browser: BrowserContext = None

    @property
    @abstractmethod
    def supermercado_id(self) -> str:
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        pass

    @abstractmethod
    def scrape_productos(
        self,
        page: Page
    ) -> list[dict]:
        pass

    # Selecciona un User-Agent aleatorio
    def obtener_user_agent(self):

        return random.choice(
            USER_AGENTS
        )

    # Delay aleatorio para simular usuario real
    def delay(self):

        segundos = random.uniform(
            self.delay_min,
            self.delay_max
        )

        logger.info(
            f"[{self.supermercado_id}] "
            f"Esperando {segundos:.1f}s"
        )

        time.sleep(segundos)

    # Inicia navegador persistente
    def iniciar_browser(self):

        self.playwright = (
            sync_playwright().start()
        )

        # Guarda cookies y sesión
        os.makedirs(
            f"./sessions/{self.supermercado_id}",
            exist_ok=True
        )

        self.browser = (
            self.playwright.chromium
            .launch_persistent_context(

                user_data_dir=(
                    f"./sessions/"
                    f"{self.supermercado_id}"
                ),

                headless=self.headless,

                args=[

                    "--disable-blink-features=AutomationControlled",

                    "--disable-dev-shm-usage",

                    "--no-sandbox",
                ],

                # Resoluciones aleatorias
                viewport={

                    "width": random.choice(
                        [1280, 1366, 1440]
                    ),

                    "height": random.choice(
                        [720, 768, 900]
                    )
                },

                locale="es-CR",

                timezone_id="America/Costa_Rica",

                user_agent=(
                    self.obtener_user_agent()
                ),
            )
        )

    def cerrar_browser(self):

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()

    # Nueva pestaña
    def nueva_pagina(self):

        page = self.browser.new_page()

        # Oculta señales básicas de automatización
        Stealth().apply_stealth_sync(page)

        page.set_extra_http_headers({

            "Accept-Language":
                "es-CR,es;q=0.9,en;q=0.8",

            "Upgrade-Insecure-Requests":
                "1",

            "DNT":
                "1",
        })

        return page

    # Simula comportamiento humano
    def comportamiento_humano(
        self,
        page: Page
    ):

        try:

            # Movimiento mouse
            page.mouse.move(

                random.randint(100, 500),

                random.randint(100, 500)
            )

            page.wait_for_timeout(
                random.randint(1000, 3000)
            )

            # Scrolls aleatorios
            for _ in range(
                random.randint(2, 5)
            ):

                page.mouse.wheel(

                    0,

                    random.randint(300, 1000)
                )

                page.wait_for_timeout(

                    random.randint(1000, 2500)
                )

        except Exception:
            pass

    def ejecutar(self) -> list[dict]:

        # Respeta robots.txt
        if not can_fetch(
            self.supermercado_id,
            "/"
        ):

            logger.warning(
                f"[{self.supermercado_id}] "
                f"Bloqueado por robots.txt"
            )

            return []

        resultados = []

        # Retries automáticos
        for intento in range(
            self.max_retries
        ):

            try:

                self.iniciar_browser()

                page = self.nueva_pagina()

                logger.info(
                    f"[{self.supermercado_id}] "
                    f"Entrando a {self.base_url}"
                )

                response = page.goto(

                    self.base_url,

                    wait_until="domcontentloaded",

                    timeout=60000
                )

                if response:

                    status = response.status

                    logger.info(
                        f"[{self.supermercado_id}] "
                        f"Status: {status}"
                    )

                    # Bloqueos típicos
                    if status in [403, 429]:

                        logger.warning(
                            f"[{self.supermercado_id}] "
                            f"Bloqueado ({status})"
                        )

                        return []

                self.delay()

                self.comportamiento_humano(
                    page
                )

                html = page.content()

                # Detecta captchas/challenges
                if detectar_bloqueo(html):

                    logger.warning(
                        f"[{self.supermercado_id}] "
                        f"Captcha detectado"
                    )

                    os.makedirs(
                        "errores",
                        exist_ok=True
                    )

                    page.screenshot(

                        path=(
                            "errores/"
                            f"{self.supermercado_id}.png"
                        )
                    )

                    return []

                productos = (
                    self.scrape_productos(page)
                )

                # Metadata común
                for p in productos:

                    p["supermercado"] = (
                        self.supermercado_id
                    )

                    p["fecha_hora"] = (
                        datetime.utcnow()
                    )

                    p["requiere_membresia"] = (
                        self.supermercado_id
                        == "pricesmart"
                    )

                resultados = productos

                logger.info(
                    f"[{self.supermercado_id}] "
                    f"{len(productos)} productos encontrados"
                )

                break

            except Exception as e:

                logger.error(
                    f"[{self.supermercado_id}] "
                    f"Intento {intento + 1} "
                    f"falló: {e}"
                )

                # Screenshot errores
                try:

                    os.makedirs(
                        "errores",
                        exist_ok=True
                    )

                    page.screenshot(

                        path=(
                            "errores/"
                            f"{self.supermercado_id}_error.png"
                        )
                    )

                except Exception:
                    pass

                # Backoff progresivo
                espera = (
                    (intento + 1)
                    * random.randint(10, 20)
                )

                logger.warning(
                    f"[{self.supermercado_id}] "
                    f"Reintentando en {espera}s"
                )

                time.sleep(espera)

            finally:

                self.cerrar_browser()

        return resultados