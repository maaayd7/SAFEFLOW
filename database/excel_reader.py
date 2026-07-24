from pathlib import Path
import pandas as pd


class ExcelReader:

    def __init__(self):

        self.base_dir = Path(__file__).resolve().parent.parent
        self.file = self.base_dir / "data" / "condiciones.xlsx"

    def load(self):

        xls = pd.ExcelFile(self.file)

        hojas = {}

        for hoja in xls.sheet_names:

            df = pd.read_excel(
                self.file,
                sheet_name=hoja,
                header=1
            )

            # Elimina la fila auxiliar que queda después del encabezado
            df = df.iloc[1:].reset_index(drop=True)

            hojas[hoja] = df

        return hojas

    def sheet_names(self):

        return pd.ExcelFile(self.file).sheet_names

    def sheet(self, nombre):

        df = pd.read_excel(
            self.file,
            sheet_name=nombre,
            header=1
        )

        df = df.iloc[1:].reset_index(drop=True)

        return df