import os

from apscheduler.schedulers.blocking import (
    BlockingScheduler
)

from backend.jobs.run_scrapers import (
    ejecutar_scrapers
)


HORAS = int(
    os.environ.get(
        "SCRAPER_INTERVAL_HOURS",
        6
    )
)

scheduler = BlockingScheduler()

# Ejecuta scrapers automáticamente
scheduler.add_job(

    ejecutar_scrapers,

    "interval",

    hours=HORAS

    #para pruebas, cada minuto
    #minutes=1   
)

print(
    f"Scheduler iniciado "
    f"cada {HORAS} horas"
)

scheduler.start()