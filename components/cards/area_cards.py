import streamlit as st


def mostrar_tarjetas(df):

    if "ÁREA" not in df.columns:
        return None

    datos = df.copy()

    # ==========================================================
    # NORMALIZAR ÁREA
    # ==========================================================

    datos["ÁREA"] = (
        datos["ÁREA"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Eliminar áreas vacías para evitar botones sin key
    datos = datos[datos["ÁREA"] != ""].copy()

    # ==========================================================
    # NORMALIZAR ESTADO
    # ==========================================================

    if "ESTADO" not in datos.columns:
        datos["ESTADO"] = ""

    datos["ESTADO"] = (
        datos["ESTADO"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    datos["ESTADO"] = datos["ESTADO"].replace({

        "ABIERTA": "ABIERTO",
        "ABIERTO": "ABIERTO",

        "CERRADA": "CERRADO",
        "CERRADO": "CERRADO",

        "EN PROCESO": "EN PROCESO",
        "EN PROCESO ": "EN PROCESO",

        "ATRASADA": "ATRASADO",
        "ATRASADO": "ATRASADO"

    })

    area_seleccionada = None

    columnas = st.columns(3)

    # ==========================================================
    # RECORRER ÁREAS
    # ==========================================================

    for i, area in enumerate(sorted(datos["ÁREA"].unique())):

        datos_area = datos[
            datos["ÁREA"] == area
        ]

        # ==========================================================
        # CONTAR CADA ESTADO
        # ==========================================================

        abiertos = len(
            datos_area[
                datos_area["ESTADO"] == "ABIERTO"
            ]
        )

        en_proceso = len(
            datos_area[
                datos_area["ESTADO"] == "EN PROCESO"
            ]
        )

        atrasados = len(
            datos_area[
                datos_area["ESTADO"] == "ATRASADO"
            ]
        )

        cerrados = len(
            datos_area[
                datos_area["ESTADO"] == "CERRADO"
            ]
        )

        total = len(datos_area)

        porcentaje = 0

        if total > 0:

            porcentaje = round(
                cerrados * 100 / total
            )

        # ==========================================================
        # COLOR DEL BORDE
        # Prioridad:
        # ATRASADO -> ROJO
        # ABIERTO -> AMARILLO
        # EN PROCESO -> AZUL
        # TODO CERRADO -> VERDE
        # ==========================================================

        if atrasados > 0:

            color_borde = "#ef4444"

        elif abiertos > 0:

            color_borde = "#facc15"

        elif en_proceso > 0:

            color_borde = "#3b82f6"

        else:

            color_borde = "#22c55e"

        # ==========================================================
        # MOSTRAR TARJETA
        # ==========================================================

        with columnas[i % 3]:

            st.markdown(
                f"""
                <div style='
                    background-color:#1f2937;
                    padding:20px;
                    border-radius:12px;
                    border-left:8px solid {color_borde};
                    margin-bottom:15px;
                '>

                    <h3 style='
                        text-align:center;
                        color:white;
                    '>
                        🏭 {area}
                    </h3>

                    <h1 style='
                        text-align:center;
                        color:#facc15;
                    '>
                        {abiertos}
                    </h1>

                    <p style='
                        text-align:center;
                        color:white;
                    '>
                        Condiciones Abiertas
                    </p>

                    <hr style='border-color:#4b5563;'>

                    <p style='color:#facc15'>
                        🟡 Abiertas: <b>{abiertos}</b>
                    </p>

                    <p style='color:#3b82f6'>
                        🔵 En Proceso: <b>{en_proceso}</b>
                    </p>

                    <p style='color:#ef4444'>
                        🔴 Atrasadas: <b>{atrasados}</b>
                    </p>

                    <p style='color:#22c55e'>
                        🟢 Cerradas: <b>{cerrados}</b>
                    </p>

                    <p style='color:white'>
                        📈 % Cierre: <b>{porcentaje}%</b>
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            # ==========================================================
            # BOTÓN
            # ==========================================================

            if st.button(
                "📂 Entrar",
                key=f"area_{i}_{area}",
                width="stretch"
            ):

                area_seleccionada = area

    return area_seleccionada
