import plotly.express as px
import pandas as pd


class ChartService:

    def __init__(self, df):

        self.df = df.copy()

        # ==================================================
        # LIMPIEZA GENERAL
        # ==================================================

        self.df.columns = (
            self.df.columns
            .astype(str)
            .str.strip()
        )

        for c in self.df.columns:

            if self.df[c].dtype == object:

                self.df[c] = (
                    self.df[c]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

        # ==================================================
        # ÁREA
        # ==================================================

        if "ÁREA" in self.df.columns:

            self.df["ÁREA"] = (
                self.df["ÁREA"]
                .str.upper()
            )

        # ==================================================
        # RESPONSABLE
        # ==================================================

        if "RESPONSABLE DE ÁREA" in self.df.columns:

            self.df["RESPONSABLE DE ÁREA"] = (
                self.df["RESPONSABLE DE ÁREA"]
                .str.upper()
            )

        # ==================================================
        # PRIORIZACIÓN
        # ==================================================

        if "PRIORIZACIÓN" in self.df.columns:

            self.df["PRIORIZACIÓN"] = (
                self.df["PRIORIZACIÓN"]
                .str.upper()
            )

        # ==================================================
        # ESTADO
        # ==================================================

        if "ESTADO" in self.df.columns:

            estado = (
                self.df["ESTADO"]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.upper()
            )

            # Normalizar estados

            estado = estado.replace({

                "ABIERTA": "ABIERTO",
                "ABIERTO ": "ABIERTO",
                " ABIERTO": "ABIERTO",

                "CERRADA": "CERRADO",
                "CERRADO ": "CERRADO",
                " CERRADO": "CERRADO",

                "0": "",
                "NAN": "",
                "NONE": "",
                "NULL": ""

            })

            # Cualquier texto que contenga CERR se vuelve CERRADO

            estado = estado.apply(
                lambda x: "CERRADO"
                if "CERR" in x
                else x
            )

            # Cualquier texto que contenga ABIER se vuelve ABIERTO

            estado = estado.apply(
                lambda x: "ABIERTO"
                if "ABIER" in x
                else x
            )

            self.df["ESTADO"] = estado

            # Eliminar registros sin estado válido

            self.df = self.df[
                self.df["ESTADO"].isin(
                    [
                        "ABIERTO",
                        "CERRADO"
                    ]
                )
            ]

    # ==================================================

    def filtrar_estado(self, estado):

        if estado == "Todas":
            return self.df.copy()

        return self.df[
            self.df["ESTADO"] == estado.upper()
        ]

    # ==================================================

    def grafico_area(self, estado="Todas"):

        df = self.filtrar_estado(estado)

        datos = (
            df.groupby(
                ["ÁREA", "ESTADO"]
            )
            .size()
            .reset_index(name="Cantidad")
        )

        fig = px.bar(

            datos,

            x="ÁREA",

            y="Cantidad",

            color="ESTADO",

            barmode="group",

            text_auto=True,

            color_discrete_map={

                "ABIERTO": "#d62728",

                "CERRADO": "#2ca02c"

            },

            title="Condiciones por Área"

        )

        fig.update_layout(

            xaxis_title="",

            yaxis_title="Cantidad",

            legend_title="Estado"

        )

        return fig

    # ==================================================

    def grafico_estado(self):

        datos = (

            self.df.groupby("ESTADO")

            .size()

            .reset_index(name="Cantidad")

        )

        fig = px.pie(

            datos,

            names="ESTADO",

            values="Cantidad",

            hole=0.45,

            color="ESTADO",

            color_discrete_map={

                "ABIERTO": "#d62728",

                "CERRADO": "#2ca02c"

            },

            title="Estado General"

        )

        return fig

    # ==================================================

    def grafico_responsables(self):

        abiertos = self.df[

            self.df["ESTADO"] == "ABIERTO"

        ]

        datos = (

            abiertos

            .groupby("RESPONSABLE DE ÁREA")

            .size()

            .reset_index(name="Cantidad")

            .sort_values(

                "Cantidad",

                ascending=False

            )

            .head(10)

        )

        fig = px.bar(

            datos,

            x="RESPONSABLE",

            y="Cantidad",

            color="Cantidad",

            text_auto=True,

            title="Top 10 Responsables con más Condiciones Abiertas"

        )

        fig.update_layout(

            showlegend=False,

            xaxis_title="",

            yaxis_title="Condiciones",

            xaxis_tickangle=-35

        )

        return fig
