from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from backend.db.database import crear_tablas

if __name__ == "__main__":
    print("Creando tablas...")
    crear_tablas()
    print("Tablas creadas exitosamente!")