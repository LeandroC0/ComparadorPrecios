import logging
import os


# Crea carpeta logs si no existe
os.makedirs("logs", exist_ok=True)


logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s "
        "[%(levelname)s] "
        "%(message)s"
    ),

    handlers=[

        logging.FileHandler(
            "logs/scraper.log",
            encoding="utf-8"
        ),

        logging.StreamHandler()
    ]
)

logger = logging.getLogger("scraper")