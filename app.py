import streamlit as st

from components.navbar import navbar

from modules.dashboard import dashboard
from modules.nuevo_reporte import nuevo_reporte
from modules.gestion import gestion
from modules.indicadores import indicadores
from modules.mapa_calor import mapa
from modules.ia import ia
from modules.configuracion import configuracion


# ======================================================
# CONFIGURACIÓN
# ======================================================

st.set_page_config(
    page_title="SAFEFLOW",
    page_icon="🦺",
    layout="wide"
)

# ======================================================
# BARRA DE NAVEGACIÓN
# ======================================================

opcion = navbar()

# ======================================================
# MÓDULOS
# ======================================================

if opcion == "🏠 Dashboard":

    dashboard()

elif opcion == "📝 Nuevo Reporte":

    nuevo_reporte()

elif opcion == "📋 Gestión":

    gestion()

elif opcion == "📊 Indicadores":

    indicadores()

elif opcion == "🗺️ Mapa":

    mapa()

elif opcion == "🤖 IA":

    ia()

elif opcion == "⚙️ Configuración":

    configuracion()