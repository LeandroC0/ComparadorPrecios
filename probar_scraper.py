from backend.scrapers.auto_mercado import (
    AutoMercadoScraper
)


print("\n=== INICIANDO SCRAPER ===\n")

scraper = AutoMercadoScraper()

productos = scraper.ejecutar()

print("\n=== RESULTADOS ===\n")

print(f"Productos encontrados: {len(productos)}")

# Muestra algunos productos
for p in productos[:5]:

    print("-" * 50)

    print(f"Nombre: {p.get('nombre')}")

    print(f"Precio: {p.get('precio')}")

    print(f"Promo: {p.get('es_promo')}")

    print(f"URL: {p.get('url')}")

    print(f"Imagen: {p.get('imagen_url')}")