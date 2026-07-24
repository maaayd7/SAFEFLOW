from services.dashboard_service import DashboardService


class IndicatorService:

    def __init__(self):

        self.dashboard = DashboardService()

        hoja = self.dashboard.hojas()[0]

        self.df = self.dashboard.dataframe(hoja)

        # Limpia nombres de columnas
        self.df.columns = (
            self.df.columns
            .astype(str)
            .str.strip()
        )

        # Limpia ESTADO
        if "ESTADO" in self.df.columns:

            self.df["ESTADO"] = (
                self.df["ESTADO"]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.lower()
            )

        # Limpia PRIORIZACIÓN
        if "PRIORIZACIÓN" in self.df.columns:

            self.df["PRIORIZACIÓN"] = (
                self.df["PRIORIZACIÓN"]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.upper()
            )

    def condiciones_abiertas(self):

        if "ESTADO" not in self.df.columns:
            return 0

        return len(
            self.df[
                self.df["ESTADO"] == "abierto"
            ]
        )

    def condiciones_cerradas(self):

        if "ESTADO" not in self.df.columns:
            return 0

        return len(
            self.df[
                self.df["ESTADO"] == "cerrado"
            ]
        )

    def criticas(self):

        if "PRIORIZACIÓN" not in self.df.columns:
            return 0

        return len(
            self.df[
                self.df["PRIORIZACIÓN"].isin(
                    [
                        "ALTA",
                        "CRÍTICA",
                        "CRITICA"
                    ]
                )
            ]
        )

    def porcentaje_cierre(self):

        total = len(self.df)

        if total == 0:
            return 0

        return round(
            self.condiciones_cerradas() * 100 / total,
            1
        )