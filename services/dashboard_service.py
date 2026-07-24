from database.excel_reader import ExcelReader


class DashboardService:

    def __init__(self):
        self.excel = ExcelReader()
        self.data = self.excel.load()

    def hojas(self):
        return self.excel.sheet_names()

    def dataframe(self, hoja):
        return self.excel.sheet(hoja)

    def resumen(self):

        resumen = []

        for hoja, df in self.data.items():

            resumen.append(
                {
                    "Hoja": hoja,
                    "Registros": len(df),
                    "Columnas": len(df.columns)
                }
            )

        return resumen