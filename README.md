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

## Ruta de desarrollo — Fases

### ✅ Fase 1 — Cimientos `[en progreso]`

| Paso | Tarea | Criterio de exito |
|------|-------|-------------------|
| 1.1 | Schema PostgreSQL + modelos SQLAlchemy | Migraciones corren sin error |
| 1.2 | `robots.py` — validacion robots.txt reutilizable | `can_fetch()` retorna bool correcto |
| 1.3 | `base_scraper.py` — Playwright + User-Agent + delay | Instanciable sin errores, delay en logs |
| 1.4 | Scraper Auto Mercado — nombre, precio, promo, imagen_url | Retorna lista con todos los campos |
| 1.5 | Scheduler con 2 ciclos diarios + ciclo manual para testing | Ciclo manual guarda datos en DB |
| 1.6 | API basica: `GET /productos` y `GET /comparar/{id}` | Responde JSON con imagen_url incluida |

---

### 📋 Fase 2 — Scrapers restantes `[pendiente]`

| Paso | Tarea | Criterio de exito |
|------|-------|-------------------|
| 2.1 | Scraper Walmart | Datos en DB, imagen_url valida |
| 2.2 | Scraper Maxi Pali | Datos en DB, imagen_url valida |
| 2.3 | Scraper MegaSuper | Datos en DB, imagen_url valida |
| 2.4 | Scraper Mayca (filtrar equivalentes de consumo) | Datos en DB, imagen_url valida |
| 2.5 | Scraper PriceSmart — solo precios publicos, `requiere_membresia=true` | Sin ningun tipo de login |

---

### 📋 Fase 3 — Frontend base `[pendiente]`

| Paso | Tarea | Criterio de exito |
|------|-------|-------------------|
| 3.1 | Monitor de Precios — cards con imagen y mejor precio | Cards con fallback a placeholder |
| 3.2 | Comparador — tabla por supermercado + grafico historial | Badge naranja de membresia en PriceSmart |
| 3.3 | Busqueda en tiempo real por nombre/categoria | Filtra mientras se escribe |
| 3.4 | Disclaimer global: _"Precios referenciales. Verificar en tienda."_ | Visible en todas las vistas |

---

### 📋 Fase 4 — Inteligencia y alertas `[pendiente]`

| Paso | Tarea | Criterio de exito |
|------|-------|-------------------|
| 4.1 | Detector de cambios — bajada %, `promo_temporal`, `precio_minimo_30d` | Badges correctos en frontend |
| 4.2 | Alertas Telegram — precio anterior/nuevo + link + imagen | Mensaje llega al chat |
| 4.3 | Alertas Email via SMTP (opcional) | Email con formato correcto |
| 4.4 | `POST /alertas` para configurar alertas por producto | Alerta dispara en siguiente ciclo |

---

### 📋 Fase 5 — Carrito y analytics `[pendiente]`

| Paso | Tarea | Criterio de exito |
|------|-------|-------------------|
| 5.1 | Algoritmo carrito optimo — precio + costo de viaje | Retorna combinacion mas barata |
| 5.2 | Vista Carrito Optimo con seleccion de productos | Muestra ahorro vs una sola tienda |
| 5.3 | Vista Compra Final — lista por supermercado con links | Links abren el producto correcto |
| 5.4 | Analytics — dia mas barato, ranking tiendas, tendencias | Graficos Recharts sin errores |

---

### 📋 Fase 6 — Pulido y produccion `[pendiente]`

| Paso | Tarea | Criterio de exito |
|------|-------|-------------------|
| 6.1 | PWA — manifest.json + service worker | Instalable en Android/iOS |
| 6.2 | Particionamiento tabla `precios` si supera 10M filas | Query historial < 200ms |
| 6.3 | Logging centralizado de ciclos | Log consultable por ciclo |
| 6.4 | Manejo de fallo de imagen_url | Nunca se ve imagen rota |
| 6.5 | Optimizaciones de performance | Lighthouse > 80 en movil |

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
