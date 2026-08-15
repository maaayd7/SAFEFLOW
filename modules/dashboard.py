import streamlit as st
import pandas as pd
from services.dashboard_service import DashboardService
from services.filter_service import FilterService
from services.chart_service import ChartService

from components.cards.area_cards import mostrar_tarjetas


def dashboard():

    dashboard_service = DashboardService()

    hoja = dashboard_service.hojas()[0]
    
    # Cargar Excel
    df_original = dashboard_service.dataframe(hoja)
    
    # Normalizar áreas y estados
    filtro = FilterService(df_original)
    
    # Este se usará para TARJETAS y DETALLE
    df_normalizado = filtro.df.copy()
    
    # Copia para filtros, indicadores y gráficos
    df = df_normalizado.copy()
    

    # ==========================================================
    # FILTROS
    # ==========================================================

    st.subheader("Filtros")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        area = st.selectbox(
            "Área",
            ["TODAS"] + (
                sorted(df["ÁREA"].dropna().unique().tolist())
                if "ÁREA" in df.columns
                else []
            ),
            key="filtro_area"
        )
    
    with c2:
        estado = st.selectbox(
            "Estado",
            [
                "TODOS",
                "ABIERTO",
                "EN PROCESO",
                "ATRASADO",
                "CERRADO"
            ],
            key="filtro_estado"
        )
    
    with c3:
        responsable = st.selectbox(
            "Responsable",
            ["TODOS"] + (
                sorted(
                    df["RESPONSABLE DE ÁREA"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
                if "RESPONSABLE DE ÁREA" in df.columns
                else []
            ),
            key="filtro_responsable"
        )
    
    with c4:
        prioridad = st.selectbox(
            "Priorización",
            ["TODAS"] + (
                sorted(
                    df["PRIORIZACIÓN"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
                if "PRIORIZACIÓN" in df.columns
                else []
            ),
            key="filtro_prioridad"
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
        df_dashboard[df_dashboard["ESTADO"] == "ABIERTO"]
    )
    
    en_proceso = len(
        df_dashboard[df_dashboard["ESTADO"] == "EN PROCESO"]
    )
    
    atrasadas = len(
        df_dashboard[df_dashboard["ESTADO"] == "ATRASADO"]
    )
    
    cerradas = len(
        df_dashboard[df_dashboard["ESTADO"] == "CERRADO"]
    )
    
    criticas = len(
        df_dashboard[
            df_dashboard["PRIORIZACIÓN"]
            .fillna("")
            .astype(str)
            .str.upper()
            .isin([
                "ALTA",
                "CRÍTICA",
                "CRITICA"
            ])
        ]
    )
    
    porcentaje = round(
        cerradas * 100 / len(df_dashboard),
        1
    ) if len(df_dashboard) > 0 else 0

    st.divider()

    k1, k2, k3, k4, k5, k6 = st.columns(6)

    k1.metric("🔴 Abiertas", abiertas)
    
    k2.metric("🟡 En Proceso", en_proceso)
    
    k3.metric("🔴 Atrasadas", atrasadas)
    
    k4.metric("🟢 Cerradas", cerradas)
    
    k5.metric("⚠️ Críticas", criticas)
    
    k6.metric("% Cierre", f"{porcentaje}%")

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

    area_card = mostrar_tarjetas(df_normalizado)

    # ==========================================================
    # DETALLE DEL ÁREA SELECCIONADA
    # ==========================================================

    if area_card:

        pendientes = df_normalizado[
            (
                df_normalizado["ÁREA"] == area_card
            )
            &
            (
                df_normalizado["ESTADO"].isin([
                    "ABIERTO",
                    "EN PROCESO",
                    "ATRASADO"
                ])
            )
        ].copy()

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
        
            (pendientes["ESTADO"].isin([
                "ABIERTO",
                "EN PROCESO",
                "ATRASADO"
            ]))
        
        ].copy()

        st.divider()

        st.subheader(

            f"Condiciones Pendientes - {area_card}"

        )

        if len(pendientes) == 0:

            st.success(

                "No existen condiciones abiertas, en proceso o atrasadas para esta área."

            )

        else:

            # ==========================================================
# COLUMNAS A MOSTRAR
# ==========================================================

            columnas_deseadas = [

                "NÚMERO",
            
                "FECHA DEL REPORTE",
            
                "ACCIÓN/ CONDICIÓN",
            
                "Detalle",
            
                "RIESGOS",
            
                "PRIORIZACIÓN",
            
                "ÁREA",
            
                "LUGAR / MAQUINA / EQUIPO",
            
                "RESPONSABLE DE ÁREA",
            
                "ACCION CORRECTIVA",
            
                "RESPONSABLE DE CIERRE",
            
                "FECHA PROPUESTA DE CIERRE",
            
                "ESTADO"
            
            ]

            columnas = [

                c

                for c in columnas_deseadas

                if c in pendientes.columns

            ]

            tabla = pendientes[columnas].copy()

            for columna_fecha in [

                "FECHA DEL REPORTE",

                "FECHA PROPUESTA DE CIERRE",

                "FECHA REAL DE CIERRE"

            ]:

                if columna_fecha in tabla.columns:
            
                    tabla[columna_fecha] = pd.to_datetime(
                        tabla[columna_fecha],
                        errors="coerce"
                    ).dt.strftime("%d/%m/%Y")

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

                f"Total de condiciones pendientes en {area_card}: {len(pendientes)}"

            )

    else:

        st.info(

            "Seleccione una tarjeta para visualizar únicamente las condiciones abiertas del área."

        )
