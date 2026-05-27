from datetime import (
    datetime,
    timedelta,
    timezone
)


CACHE_HORAS = 6


def necesita_actualizacion(
    ultima_actualizacion
) -> bool:
    """
    Determina si un producto
    necesita scraping nuevamente.
    """

    if not ultima_actualizacion:
        return True

    ahora = datetime.now(timezone.utc)

    diferencia = (
        ahora - ultima_actualizacion
    )

    return diferencia > timedelta(
        hours=CACHE_HORAS
    )