import streamlit as st


def mostrar_tarjetas(df):

    if "ÁREA" not in df.columns:
        return None

    datos = df.copy()

    datos["ÁREA"] = (
        datos["ÁREA"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .replace({
            "CORTE & CONFORMADO": "CORTE Y CONFORMADO",
            "CORTE  Y  CONFORMADO": "CORTE Y CONFORMADO",
            "LOGISTICA": "LOGÍSTICA",
            "MANTENIMIENTO MECANICO": "MANTENIMIENTO MECÁNICO",
            "MANTENIMIENTO ELECTRICO": "MANTENIMIENTO ELÉCTRICO"
        })
    )

    datos["ESTADO"] = (
        datos["ESTADO"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    datos["ESTADO"] = datos["ESTADO"].replace({
        "ABIERTA": "ABIERTO",
        "CERRADA": "CERRADO"
    })

    area_seleccionada = None

    columnas = st.columns(3)

    # Eliminar áreas vacías
    datos = datos[
        datos["ÁREA"] != ""
    ]
    for i, area in enumerate(sorted(datos["ÁREA"].unique())):

        abiertos = len(
            datos[
                (datos["ÁREA"] == area)
                &
                (datos["ESTADO"] == "ABIERTO")
            ]
        )
        
        en_proceso = len(
            datos[
                (datos["ÁREA"] == area)
                &
                (datos["ESTADO"] == "EN PROCESO")
            ]
        )
        
        atrasados = len(
            datos[
                (datos["ÁREA"] == area)
                &
                (datos["ESTADO"] == "ATRASADO")
            ]
        )
        
        cerrados = len(
            datos[
                (datos["ÁREA"] == area)
                &
                (datos["ESTADO"] == "CERRADO")
            ]
        )

        total = (
            abiertos
            + en_proceso
            + atrasados
            + cerrados
        )

        porcentaje = 0

        if total > 0:
            porcentaje = int(cerrados * 100 / total)

        if porcentaje >= 90:
            color = "#22c55e"
        elif porcentaje >= 70:
            color = "#f59e0b"
        else:
            color = "#ef4444"

        with columnas[i % 3]:

            st.markdown(
                f"""
<div style='
background-color:#1f2937;
padding:20px;
border-radius:12px;
border-left:8px solid {color};
margin-bottom:15px;
'>

<h3 style='text-align:center;color:white'>
🏭 {area}
</h3>

<h1 style='text-align:center;color:#ef4444'>
{abiertos}
</h1>

<p style='text-align:center;color:white'>
Condiciones Abiertas
</p>

<hr>

<p style='color:#ef4444'>
🔴 Abiertas: <b>{abiertos}</b>
</p>

<p style='color:#f59e0b'>
🟡 En Proceso: <b>{en_proceso}</b>
</p>

<p style='color:#dc2626'>
⏰ Atrasadas: <b>{atrasados}</b>
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

            if st.button(
                f"📂 Entrar",
                key=f"area_{i}",
                width="stretch"
            ):
                area_seleccionada = area

    return area_seleccionada
