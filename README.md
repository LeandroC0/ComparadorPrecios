# PreciosCR 🛒
**Monitor inteligente de precios de supermercados costarricenses**

> Extrae precios automáticamente de 6 supermercados, detecta promos, compara entre tiendas y calcula el carrito más barato.

---

## Stack

| Capa | Tecnología |
|------|-----------|
| Scraping | Python 3.11+, Playwright |
| Backend | FastAPI, APScheduler |
| Base de datos | PostgreSQL 16 (Docker) |
| ORM / Migraciones | SQLAlchemy 2.0, Alembic |
| Frontend | React 18 + Vite, TailwindCSS, Recharts, Zustand |
| Notificaciones | Telegram Bot, Email SMTP |

---

## Supermercados monitoreados

| Tienda | URL | Dificultad |
|--------|-----|-----------|
| Auto Mercado | automercado.co.cr | Baja — empezar aquí |
| MegaSuper | megasuper.net | Baja |
| Walmart | walmart.co.cr | Media |
| Maxi Palí | maxipali.co.cr | Media |
| Mayca | mayca.co.cr | Media (catálogo B2B) |
| PriceSmart ⚠ | pricesmart.com | Alta — solo precios públicos, sin login |

> ⚠ PriceSmart requiere membresía para comprar. PreciosCR muestra sus precios **solo con fines comparativos**. Se despliega un badge de advertencia en toda la interfaz.

---

## Requisitos previos

- Python 3.11+
- Docker Desktop
- Node.js 18+
- Git

---

## Instalación y arranque rápido

```bash
# 1. Clonar el proyecto
git clone https://github.com/tuusuario/preciosCR.git
cd preciosCR

# 2. Crear entorno virtual Python
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# 3. Instalar dependencias Python
pip install -r requirements.txt
playwright install chromium

# 4. Copiar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# 5. Levantar PostgreSQL con Docker
docker-compose up -d

# 6. Crear tablas en la base de datos
python probar_db.py

# 7. Instalar dependencias frontend
cd frontend
npm install
npm run dev
```

---

## Variables de entorno (`.env`)

```env
# Base de datos
DATABASE_URL=postgresql://precioscr:precioscr123@localhost:5433/precioscr

# Scraping
SCRAPING_HOUR_1=3              # Primer ciclo: 3:00 am hora CR
SCRAPING_HOUR_2=15             # Segundo ciclo: 3:00 pm hora CR
SCRAPING_DELAY_MIN=5           # Segundos minimo entre requests
SCRAPING_DELAY_MAX=10          # Segundos maximo entre requests
HEADLESS=true                  # false solo para debugging local
BOT_USER_AGENT=PreciosCR-Bot/1.0 (+https://tudominio.cr/bot)

# Alertas
ALERTA_UMBRAL_DEFAULT=10       # % de bajada para alertar
PROMO_UMBRAL=15                # Bajada > 15% = promo temporal

# Telegram (opcional)
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id

# Email (opcional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu@email.com
SMTP_PASS=tu_app_password
```

> **Nunca subas el `.env` real a Git.** El `.gitignore` ya lo excluye.

---

## Estructura del proyecto

```
preciosCR/
├── backend/
│   ├── scrapers/
│   │   ├── base_scraper.py       # Clase base con Playwright + robots.txt
│   │   ├── auto_mercado.py       # Empezar aqui
│   │   ├── walmart.py
│   │   ├── maxi_pali.py
│   │   ├── pricesmart.py
│   │   ├── megasuper.py
│   │   └── mayca.py
│   ├── db/
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── database.py           # Engine + SessionLocal
│   │   └── migrations/           # Alembic
│   ├── services/
│   │   ├── detector.py           # Detecta cambios de precio y promos
│   │   ├── alertas.py            # Motor de alertas Telegram/Email
│   │   ├── analytics.py          # Queries de analytics semanales
│   │   ├── carrito.py            # Algoritmo carrito optimo
│   │   └── robots.py             # Validacion robots.txt reutilizable
│   ├── api/
│   │   ├── main.py               # FastAPI app
│   │   └── routers/              # Un archivo por dominio
│   ├── scheduler.py              # APScheduler — 2 ciclos diarios
│   └── config.py                 # Variables de entorno
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── store/                # Zustand
│       └── api/                  # Axios calls
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Ruta de desarrollo — PreciosCR v2.0

### ✅ Fase 1 — Cimientos [en progreso]

| Paso | Tarea | Criterio de éxito |
|------|-------|-------------------|
| 1.1 | `config.py` — carga de variables de entorno con python-dotenv | Todas las vars de .env.example se leen correctamente |
| 1.2 | `docker-compose.yml` — servicios: PostgreSQL, backend, frontend | `docker compose up` levanta todo sin errores |
| 1.3 | Schema PostgreSQL + modelos SQLAlchemy (incluye `imagen_url`, `precio_por_unidad`, `requiere_membresia`) | Alembic corre `alembic upgrade head` sin error |
| 1.4 | `robots.py` — validación robots.txt reutilizable | `can_fetch()` retorna bool correcto para cada dominio objetivo |
| 1.5 | `base_scraper.py` — Playwright + User-Agent propio + delay 5–10s + perfil persistente (cookies) | Instanciable, delay verificable en logs, perfil persiste entre sesiones |
| 1.6 | Scraper Auto Mercado — nombre, precio, precio_por_unidad, unidad, es_promo, imagen_url | Retorna lista con todos los campos, imagen_url válida |
| 1.7 | Scheduler con 2 ciclos diarios (3am/3pm) + ciclo manual para testing | Ciclo manual ejecuta, guarda datos en DB, log generado |
| 1.8 | API básica: `GET /productos` y `GET /comparar/{id}` | Responde JSON con imagen_url y precio_por_unidad incluidos |
| 1.9 | `.env.example` con todas las variables documentadas | Cualquier dev puede arrancar copiando el archivo |

---

### 📋 Fase 2 — Scrapers restantes [pendiente]

| Paso | Tarea | Criterio de éxito |
|------|-------|-------------------|
| 2.1 | Scraper Walmart — nombre, precio, precio_por_unidad, unidad, promo, imagen_url | Datos en DB con todos los campos, imagen_url válida |
| 2.2 | Scraper Maxi Palí — ídem | Datos en DB con todos los campos, imagen_url válida |
| 2.3 | Scraper MegaSuper — ídem | Datos en DB con todos los campos, imagen_url válida |
| 2.4 | Scraper Mayca — ídem, filtrar solo equivalentes de consumo (no B2B puro) | Datos en DB, productos tienen par en otra tienda |
| 2.5 | Scraper PriceSmart — solo precios públicos, `requiere_membresia=true`, sin ningún login | Datos en DB con flag activo, nunca toca autenticación |
| 2.6 | Test de schema unificado — todos los scrapers retornan exactamente los mismos campos | Script de validación pasa para las 6 tiendas |
| 2.7 | Mecanismo de fallo: deshabilitar scraper tras 3 ciclos fallidos + alerta Telegram | Telegram recibe notificación, scraper se omite en ciclo siguiente |

---

### 📋 Fase 3 — Frontend base [pendiente]

| Paso | Tarea | Criterio de éxito |
|------|-------|-------------------|
| 3.1 | Setup proyecto React + Vite + TailwindCSS + Axios + react-query + Zustand | `npm run dev` sin errores, react-query devtools visible |
| 3.2 | Componente `react-image-fallback` configurado globalmente con placeholder | Imagen rota nunca visible en ninguna vista |
| 3.3 | Componente badge PriceSmart — badge naranja "⚠ Requiere membresía" | Visible sin hover en todas las vistas donde aparezca PriceSmart |
| 3.4 | Disclaimer global en layout — "Precios referenciales. Verificar en tienda." + "PreciosCR no tiene relación comercial con los supermercados." | Visible en todas las vistas sin scroll |
| 3.5 | Vista Monitor de Precios — cards por categoría con imagen y mejor precio | Cards con fallback, badge PriceSmart funcional |
| 3.6 | Vista Comparador — tabla por supermercado + gráfico historial (Recharts) | Badge naranja visible, gráfico renderiza sin errores |
| 3.7 | `GET /productos/{id}/historial` — endpoint + integración en Comparador | Historial aparece en gráfico con datos reales |
| 3.8 | `GET /buscar?q=` — endpoint + búsqueda en tiempo real por nombre/categoría | Filtra mientras se escribe, resultados con imagen |

---

### 📋 Fase 4 — Inteligencia y alertas [pendiente]

| Paso | Tarea | Criterio de éxito |
|------|-------|-------------------|
| 4.1 | `detector.py` — comparar precio nuevo vs último registrado, marcar `promo_temporal` y `precio_minimo_30d` | Flags guardados correctamente en DB tras ciclo de prueba |
| 4.2 | Badges en frontend para `promo_temporal` y `precio_minimo_30d` | Badges visibles en Monitor y Comparador con datos reales |
| 4.3 | `alertas.py` — motor Telegram: precio anterior/nuevo + link + imagen del producto | Mensaje llega al chat con formato correcto |
| 4.4 | `alertas.py` — motor Email vía SMTP (opcional) | Email recibido con formato correcto |
| 4.5 | `POST /alertas` — crear alerta por producto con umbral configurable | Alerta se crea en DB y dispara en el siguiente ciclo |

---

### 📋 Fase 5 — Carrito y analytics [pendiente]

| Paso | Tarea | Criterio de éxito |
|------|-------|-------------------|
| 5.1 | `carrito.py` — algoritmo carrito óptimo: precio + `costo_viaje_estimado` configurable | Retorna combinación más barata con desglose por tienda |
| 5.2 | `GET /carrito/optimo` — endpoint con parámetro `costo_viaje` | Responde JSON con ahorro calculado vs. una sola tienda |
| 5.3 | Vista Carrito Óptimo — selección de productos (con imagen), slider de costo de viaje, cálculo en tiempo real | Muestra ahorro numérico vs. comprar todo en tienda más cara |
| 5.4 | Vista Compra Final — lista organizada por supermercado con links directos | Links abren el producto correcto en la tienda |
| 5.5 | `analytics.py` — queries: día más barato, ranking tiendas, tendencias semanales | Queries corren en < 500ms con datos reales |
| 5.6 | `GET /analytics/semanal` + Vista Analytics con gráficos Recharts | Gráficos renderizan sin errores con datos reales |

---

### 📋 Fase 6 — Pulido y producción [pendiente]

| Paso | Tarea | Criterio de éxito |
|------|-------|-------------------|
| 6.1 | Lazy loading de imágenes en todas las vistas | Lighthouse performance > 80 en móvil |
| 6.2 | react-query cache configurado correctamente (stale time, refetch intervals) | No hay requests duplicados innecesarios en Network tab |
| 6.3 | Particionamiento tabla `precios` por fecha si supera 10M filas | Query de historial < 200ms |
| 6.4 | Logging centralizado de ciclos — qué se extrajo, cuántos requests por tienda, errores | Log consultable por ciclo, sirve como evidencia de uso razonable |
| 6.5 | Manejo de fallo de imagen_url — caché del último URL válido por producto/tienda | Nunca se muestra imagen rota, placeholder aparece consistentemente |
| 6.6 | PWA — manifest.json + service worker + íconos | Instalable en Android/iOS, Lighthouse PWA checklist pasa |
| 6.7 | `README.md` — instalación, variables de entorno, cómo correr scrapers manualmente | Un dev nuevo puede levantar el proyecto sin preguntar nada |
---

## API — Endpoints principales

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/productos` | Lista con precio mas reciente e imagen_url |
| GET | `/productos/{id}/historial` | Historial de precios por producto |
| GET | `/comparar/{id}` | Precios en todos los supermercados |
| GET | `/carrito/optimo` | Combinacion mas barata considerando costo de viaje |
| GET | `/analytics/semanal` | Dia mas barato, ranking tiendas, tendencias |
| POST | `/alertas` | Crear alerta de precio |
| GET | `/buscar?q=` | Busqueda por nombre o categoria |

---

## Comandos utiles

```bash
# Levantar DB
docker-compose up -d

# Bajar DB
docker-compose down

# Ver logs del contenedor
docker logs precioscr_db

# Conectarse a la DB directamente
docker exec -it precioscr_db psql -U precioscr -d precioscr

# Ver tablas
\dt

# Correr el scraper manualmente (una vez listo)
python -m backend.scrapers.auto_mercado

# Correr el scheduler
python backend/scheduler.py

# Correr la API
uvicorn backend.api.main:app --reload
```

---

## Buenas practicas de scraping

| Practica | Descripcion | Obligatorio |
|----------|-------------|-------------|
| Respetar robots.txt | `can_fetch()` antes de cada ciclo | **Si** |
| User-Agent propio | `PreciosCR-Bot/1.0 (+https://tudominio.cr/bot)` | **Si** |
| Delay 5–10s entre requests | Nunca bajar de 5s en produccion | **Si** |
| Scraping secuencial | Una tienda a la vez, nunca en paralelo | **Si** |
| Horarios fuera de pico | 3am y 3pm hora CR | **Si** |
| PriceSmart sin login | Solo precios publicos visibles | **Obligatorio** |

---

## Notas legales

- PreciosCR extrae **solo datos publicos** (nombre, precio, imagen visible sin login).
- Las imagenes se muestran como **URL externa**, nunca se almacenan localmente.
- No se procesan compras ni se almacenan datos personales en v1.0.
- Si se monetiza: constituir S.R.L., registrar en Hacienda, facturacion CABYS. Si se agrega registro de usuarios: cumplir Ley 8968 (PRODHAB).

---

## Disclaimer

> Los precios mostrados son referenciales. PreciosCR no tiene relacion comercial con ninguno de los supermercados listados. Verificar el precio final en cada tienda antes de comprar.

---

*PreciosCR — v2.0 — Mayo 2026*
