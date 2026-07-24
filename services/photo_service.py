from pathlib import Path
from datetime import datetime


class PhotoService:

    def __init__(self):

        self.base = (
            Path(__file__).resolve().parent.parent
            / "uploads"
        )

    def guardar(self, foto):

        if foto is None:
            return ""

        hoy = datetime.now()

        carpeta = (
            self.base
            / str(hoy.year)
            / f"{hoy.month:02d}"
        )

        carpeta.mkdir(
            parents=True,
            exist_ok=True
        )

        nombre = (
            hoy.strftime("%Y%m%d_%H%M%S_")
            + foto.name
        )

        ruta = carpeta / nombre

        with open(ruta, "wb") as f:

            f.write(foto.getbuffer())

        return str(ruta)