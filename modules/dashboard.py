import streamlit as st
import pandas as pd
from services.dashboard_service import DashboardService
from services.filter_service import FilterService
from services.chart_service import ChartService

from components.cards.area_cards import mostrar_tarjetas


def dashboard():

    dashboard_service = DashboardService()

    hoja = dashboard_service.hojas()[0]

    df_original = dashboard_service.dataframe(hoja)

    filtro = FilterService(df_original)

    df = filtro.df

    # ==========================================================
    # FILTROS
    # ==========================================================

    st.subheader("Filtros")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        area = st.selectbox(

            "Área",

            ["TODAS"] +

            sorted(df["ÁREA"].dropna().unique().tolist())

        )

    with c2:

        estado = st.selectbox(

            "Estado",

            [

                "TODOS",

                "ABIERTO",

                "CERRADO"

            ]

        )

    with c3:

        responsable = st.selectbox(

            "Responsable",

            ["TODOS"] +

            sorted(df["RESPONSABLE"].dropna().unique().tolist())

        )

    with c4:

        prioridad = st.selectbox(

            "Priorización",

            ["TODAS"] +

            sorted(df["PRIORIZACIÓN"].dropna().unique().tolist())

        )

    # ==========================================================
    # FILTROS GENERALES
    # (SOLO KPIs Y GRÁFICOS)
    # ==========================================================

    df_dashboard = filtro.aplicar(

        area,

        estado,

        responsable,

        prioridad

    )

    abiertas = len(

        df_dashboard[
            df_dashboard["ESTADO"] == "ABIERTO"
        ]

    )

    cerradas = len(

        df_dashboard[
            df_dashboard["ESTADO"] == "CERRADO"
        ]

    )

    if "PRIORIZACIÓN" in df_dashboard.columns:

        criticas = len(

            df_dashboard[

                df_dashboard["PRIORIZACIÓN"]

                .str.upper()

                .isin(

                    [

                        "ALTA",

                        "CRÍTICA",

                        "CRITICA"

                    ]

                )

            ]

        )

    else:

        criticas = 0

    porcentaje = 0

    if len(df_dashboard) > 0:

        porcentaje = round(

            cerradas * 100 / len(df_dashboard),

            1

        )

    st.divider()

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(

        "🔴 Abiertas",

        abiertas

    )

    k2.metric(

        "🟢 Cerradas",

        cerradas

    )

    k3.metric(

        "⚠️ Críticas",

        criticas

    )

    k4.metric(

        "% Cierre",

        f"{porcentaje}%"

    )

    # ==========================================================
    # GRÁFICOS
    # (SOLO FILTROS GENERALES)
    # ==========================================================

    graficos = ChartService(df_dashboard)

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.plotly_chart(

            graficos.grafico_area(),

            width="stretch"

        )

    with c2:

        st.plotly_chart(

            graficos.grafico_estado(),

            width="stretch"

        )

    st.plotly_chart(

        graficos.grafico_responsables(),

        width="stretch"

    )

        # ==========================================================
    # TARJETAS POR ÁREA
    # (NO AFECTAN KPIs NI GRÁFICOS)
    # ==========================================================

    st.divider()

    st.subheader("Condiciones por Área")

    area_card = mostrar_tarjetas(df_original)

    # ==========================================================
    # DETALLE DEL ÁREA SELECCIONADA
    # ==========================================================

    if area_card:

        pendientes = df_original.copy()

        pendientes["ÁREA"] = (

            pendientes["ÁREA"]

            .fillna("")

            .astype(str)

            .str.strip()

            .str.upper()

        )

        pendientes["ESTADO"] = (

            pendientes["ESTADO"]

            .fillna("")

            .astype(str)

            .str.strip()

            .str.upper()

        )

        pendientes["ESTADO"] = pendientes["ESTADO"].replace(

            {

                "ABIERTA": "ABIERTO",

                "CERRADA": "CERRADO"

            }

        )

        pendientes = pendientes[

            (pendientes["ÁREA"] == area_card)

            &

            (pendientes["ESTADO"] == "ABIERTO")

        ]

        st.divider()

        st.subheader(

            f"Condiciones Abiertas - {area_card}"

        )

        if len(pendientes) == 0:

            st.success(

                "No existen condiciones abiertas para esta área."

            )

        else:

            # ==========================================================
# COLUMNAS A MOSTRAR
# ==========================================================

            columnas_deseadas = [

                "FECHA DEL REPORTE",
                "ACCIÓN/ CONDICIÓN",
                "DETALLE",
                "LUGAR / MAQUINA / EQUIPO",
                "POSIBLES CONCECUENCIAS",
                "ÁREA",
                "RESPONSABLE",
                "ACCION CORRECTIVA",
                "ESTADO"

            ]

            columnas = [

                c

                for c in columnas_deseadas

                if c in pendientes.columns

            ]

            tabla = pendientes[columnas].copy()

    # ============================================
    # FORMATEAR FECHA
    # ============================================

            if "FECHA DEL REPORTE" in tabla.columns:

                try:

                    if pd.api.types.is_numeric_dtype(tabla["FECHA DEL REPORTE"]):

                        tabla["FECHA DEL REPORTE"] = pd.to_datetime(

                            tabla["FECHA DEL REPORTE"],

                            unit="D",

                            origin="1899-12-30"

                        ).dt.strftime("%d/%m/%Y")

                    else:

                        tabla["FECHA DEL REPORTE"] = pd.to_datetime(

                            tabla["FECHA DEL REPORTE"],

                            errors="coerce"

                        ).dt.strftime("%d/%m/%Y")

                except Exception:

                    pass

            st.dataframe(

                tabla,

                hide_index=True,

                width="stretch"

            )

            st.caption(

                f"Total de condiciones abiertas en {area_card}: {len(pendientes)}"

            )

    else:

        st.info(

            "Seleccione una tarjeta para visualizar únicamente las condiciones abiertas del área."

        )