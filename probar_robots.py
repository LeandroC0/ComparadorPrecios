from backend.services.robots import can_fetch, ver_robots

print("=== robots.txt de Auto Mercado ===")
ver_robots("auto_mercado")

print("\n=== Verificacion por tienda ===")
supermercados = ["walmart", "maxi_pali", "auto_mercado", "pricesmart", "megasuper", "mayca"]
for tienda in supermercados:
    resultado = can_fetch(tienda, "/")
    estado = "OK" if resultado else "BLOQUEADO"
    print(f"  {tienda:15} -> {estado}")