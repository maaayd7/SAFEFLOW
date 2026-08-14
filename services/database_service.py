from database.excel_reader import ExcelReader


class DashboardService:

    _cache = None

    def __init__(self):

        self.reader = ExcelReader()

        if DashboardService._cache is None:

            DashboardService._cache = self.reader.load()

        self.data = DashboardService._cache

    def actualizar(self):

        DashboardService._cache = self.reader.load()

        self.data = DashboardService._cache

    def hojas(self):

        return list(self.data.keys())

    def dataframe(self, hoja):

        if hoja in self.data:

            return self.data[hoja].copy()

        raise ValueError(
            f"No existe la hoja {hoja}"
        )

    def resumen(self):

        resumen = []

        for hoja, df in self.data.items():

            resumen.append({

                "Hoja": hoja,

                "Registros": len(df),

                "Columnas": len(df.columns)

            })

        return resumen
