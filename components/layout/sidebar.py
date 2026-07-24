from streamlit_option_menu import option_menu


def sidebar():

    selected = option_menu(
        menu_title="SAFEFLOW",
        options=[
            "Dashboard",
            "Reportes",
            "Nuevo Reporte",
            "Indicadores",
            "Configuración"
        ],
        icons=[
            "speedometer2",
            "list-task",
            "plus-circle",
            "bar-chart",
            "gear"
        ],
        default_index=0
    )

    return selected