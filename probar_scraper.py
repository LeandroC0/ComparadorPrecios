from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from backend.scrapers.auto_mercado import AutoMercadoScraper

if __name__ == "__main__":
    scraper = AutoMercadoScraper()
    productos = scraper.ejecutar()

    print(f"\nTotal: {len(productos)} productos")
    for p in productos[:5]:
        print(f"  {p['nombre']} - {p['precio']}")
        