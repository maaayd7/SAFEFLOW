import streamlit as st


def navbar():

    st.title("🦺 SAFEFLOW")

    opcion = st.radio(

        "Navegación",

        [

            "🏠 Dashboard",

            "📝 Nuevo Reporte",

            "📋 Gestión",

            "📊 Indicadores",

            "🗺️ Mapa",

            "🤖 IA",

            "⚙️ Configuración"

        ],

        horizontal=True,

        label_visibility="collapsed"

    )

    st.divider()

    return opcion