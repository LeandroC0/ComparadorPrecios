import random

from backend.scrapers.auto_mercado import (
    AutoMercadoScraper
)


SCRAPERS = [

    AutoMercadoScraper(),

]


def ejecutar_scrapers():

    scrapers = SCRAPERS.copy()

    # Orden aleatorio
    random.shuffle(scrapers)

    for scraper in scrapers:

        scraper.ejecutar()