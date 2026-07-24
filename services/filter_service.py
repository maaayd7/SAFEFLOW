import pandas as pd


class FilterService:

    def __init__(self, df):

        self.df = df.copy()

        self.df.columns = (
            self.df.columns
            .astype(str)
            .str.strip()
        )

        # --------------------------
        # LIMPIEZA
        # --------------------------

        for columna in self.df.columns:

            if self.df[columna].dtype == object:

                self.df[columna] = (
                    self.df[columna]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

        # ÁREA

        if "ÁREA" in self.df.columns:

            self.df["ÁREA"] = (
                self.df["ÁREA"]
                .str.upper()
            )

        # RESPONSABLE

        if "RESPONSABLE" in self.df.columns:

            self.df["RESPONSABLE"] = (
                self.df["RESPONSABLE"]
                .str.upper()
            )

        # ESTADO

        if "ESTADO" in self.df.columns:

            estado = (
                self.df["ESTADO"]
                .str.upper()
            )

            estado = estado.replace({

                "ABIERTA":"ABIERTO",
                "ABIERTO ":"ABIERTO",
                " ABIERTO":"ABIERTO",

                "CERRADA":"CERRADO",
                "CERRADO ":"CERRADO",
                " CERRADO":"CERRADO"

            })

            self.df["ESTADO"] = estado

    # ----------------------------------------

    def aplicar(
        self,
        area,
        estado,
        responsable,
        prioridad
    ):

        df = self.df.copy()

        if area != "TODAS":

            df = df[
                df["ÁREA"] == area
            ]

        if estado != "TODOS":

            df = df[
                df["ESTADO"] == estado
            ]

        if responsable != "TODOS":

            df = df[
                df["RESPONSABLE"] == responsable
            ]

        if prioridad != "TODAS":

            df = df[
                df["PRIORIZACIÓN"] == prioridad
            ]

        return df