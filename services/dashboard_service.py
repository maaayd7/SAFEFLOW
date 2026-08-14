from database.excel_reader import ExcelReader


class DashboardService:

    _cache = None

    def __init__(self):

        self.reader = ExcelReader()

        if DashboardService._cache is None:

            DashboardService._cache = self.reader.load()

        self.data = DashboardService._cache

    # ==================================================
    # ACTUALIZAR DATOS
    # ==================================================

    def actualizar(self):

        DashboardService._cache = self.reader.load()

        self.data = DashboardService._cache

    # ==================================================
    # OBTENER HOJAS
    # ==================================================

    def hojas(self):

        return list(self.data.keys())

    # ==================================================
    # OBTENER DATAFRAME
    # ==================================================

    def dataframe(self, hoja):

        if hoja in self.data:

            return self.data[hoja].copy()

        raise ValueError(f"No existe la hoja {hoja}")

    # ==================================================
    # RESUMEN
    # ==================================================

    def resumen(self):

        resumen = []

        for hoja, df in self.data.items():

            resumen.append({

                "Hoja": hoja,

                "Registros": len(df),

                "Columnas": len(df.columns)

            })

        return resumen
