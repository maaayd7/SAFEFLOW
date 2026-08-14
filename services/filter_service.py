import pandas as pd


class FilterService:

    def __init__(self, df):

        self.df = df.copy()

        # ==========================================
        # LIMPIAR NOMBRES DE COLUMNAS
        # ==========================================

        self.df.columns = (
            self.df.columns
            .astype(str)
            .str.strip()
        )

        # ==========================================
        # NORMALIZAR ÁREAS
        # ==========================================

        if "ÁREA" in self.df.columns:

            self.df["ÁREA"] = (
                self.df["ÁREA"]
                .fillna("")
                .astype(str)
                .str.upper()
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .replace({

                    "CORTE & CONFORMADO": "CORTE Y CONFORMADO",

                    "CORTE Y CONFORMADO": "CORTE Y CONFORMADO",

                    "LOGISTICA": "LOGÍSTICA",

                    "MANTENIMIENTO MECANICO": "MANTENIMIENTO MECÁNICO",

                    "MANTENIMIENTO ELECTRICO": "MANTENIMIENTO ELÉCTRICO"

                })
            )

        # ==========================================
        # NORMALIZAR ESTADOS
        # ==========================================

        if "ESTADO" in self.df.columns:

            self.df["ESTADO"] = (
                self.df["ESTADO"]
                .fillna("ABIERTO")
                .astype(str)
                .str.upper()
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .replace({

                    "ABIERTA": "ABIERTO",

                    "ABIERTO": "ABIERTO",

                    "EN PROCESO": "EN PROCESO",

                    "ENPROCESO": "EN PROCESO",

                    "CERRADA": "CERRADO",

                    "CERRADO": "CERRADO"

                })
            )

        # ==========================================
        # NORMALIZAR FECHA PROPUESTA DE CIERRE
        # ==========================================

        if "FECHA PROPUESTA DE CIERRE" in self.df.columns:

            self.df["FECHA PROPUESTA DE CIERRE"] = (
                pd.to_datetime(
                    self.df["FECHA PROPUESTA DE CIERRE"],
                    errors="coerce",
                    dayfirst=True
                )
            )

        # ==========================================
        # CALCULAR ATRASADOS
        # ==========================================

        if (
            "ESTADO" in self.df.columns
            and "FECHA PROPUESTA DE CIERRE" in self.df.columns
        ):

            hoy = pd.Timestamp.today().normalize()

            atrasados = (

                self.df["ESTADO"].isin([
                    "ABIERTO",
                    "EN PROCESO"
                ])

                &

                self.df["FECHA PROPUESTA DE CIERRE"].notna()

                &

                (
                    self.df["FECHA PROPUESTA DE CIERRE"]
                    < hoy
                )
            )

            self.df.loc[
                atrasados,
                "ESTADO"
            ] = "ATRASADO"

    # ==========================================
    # APLICAR FILTROS
    # ==========================================

    def aplicar(

        self,

        area="TODAS",

        estado="TODOS",

        responsable="TODOS",

        prioridad="TODAS"

    ):

        df = self.df.copy()

        # ÁREA

        if area != "TODAS":

            df = df[
                df["ÁREA"] == area
            ]

        # ESTADO

        if estado != "TODOS":

            df = df[
                df["ESTADO"] == estado
            ]

        # RESPONSABLE

        if (
            responsable != "TODOS"
            and "RESPONSABLE DE ÁREA" in df.columns
        ):

            df = df[
                df["RESPONSABLE DE ÁREA"] == responsable
            ]

        # PRIORIDAD

        if (
            prioridad != "TODAS"
            and "PRIORIZACIÓN" in df.columns
        ):

            df = df[
                df["PRIORIZACIÓN"] == prioridad
            ]

        return df
