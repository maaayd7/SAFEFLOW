import pandas as pd
from pathlib import Path


class ExcelReader:

    def __init__(self):

        self.base = Path(__file__).resolve().parent.parent

        self.ruta = self.base / "data" / "condiciones.xlsx"

    def load(self):

        df = pd.read_excel(
            self.ruta,
            sheet_name="Base",
            header=1
        )

        # ==========================================
        # LIMPIAR NOMBRES DE COLUMNAS
        # ==========================================

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        return {
            "Base": df
        }
