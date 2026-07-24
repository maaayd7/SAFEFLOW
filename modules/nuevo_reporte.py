import streamlit as st
from datetime import datetime

from services.excel_writer import ExcelWriter
from services.photo_service import PhotoService
from services.dashboard_service import DashboardService


def nuevo_reporte():

    st.title("📝 Nuevo Reporte")

    st.divider()

    writer = ExcelWriter()

    photo = PhotoService()

    with st.form("nuevo_reporte", clear_on_submit=True):

        c1, c2 = st.columns(2)

        with c1:

            fecha = st.date_input(
                "Fecha",
                datetime.today()
            )

            reportado_por = st.text_input(
                "Reportado por"
            )

            area = st.selectbox(
                "Área",
                [
                    "CORTE Y CONFORMADO",
                    "SOLDADURA",
                    "PANELES",
                    "VIALES",
                    "LOGÍSTICA",
                    "MANTENIMIENTO",
                    "PROYECTOS"
                ]
            )

            lugar = st.text_input("Lugar")

            maquina = st.text_input("Máquina")

        with c2:

            tipo = st.selectbox(
                "Tipo",
                [
                    "CONDICIÓN INSEGURA",
                    "ACCIÓN INSEGURA"
                ]
            )

            responsable = st.text_input(
                "Responsable"
            )

            prioridad = st.selectbox(
                "Priorización",
                [
                    "BAJA",
                    "MEDIA",
                    "ALTA",
                    "CRÍTICA"
                ]
            )

            estado = st.selectbox(
                "Estado",
                [
                    "ABIERTO",
                    "CERRADO"
                ]
            )

            fecha_compromiso = st.date_input(
                "Fecha compromiso"
            )

        descripcion = st.text_area(
            "Descripción"
        )

        consecuencia = st.text_area(
            "Consecuencia Potencial"
        )

        foto = st.file_uploader(
            "Fotografía",
            type=["jpg", "jpeg", "png"]
        )

        guardar = st.form_submit_button(
            "💾 Guardar Reporte",
            width="stretch"
        )

        if guardar:

            if reportado_por == "":
                st.error("Ingrese el nombre del reportante.")
                st.stop()

            if descripcion == "":
                st.error("Ingrese la descripción.")
                st.stop()

            ruta_foto = photo.guardar(foto)

            writer.guardar_reporte(

                fecha.strftime("%d/%m/%Y"),

                reportado_por,

                area,

                lugar,

                maquina,

                tipo,

                descripcion,

                consecuencia,

                responsable,

                prioridad,

                estado,

                fecha_compromiso.strftime("%d/%m/%Y"),

                ruta_foto

            )

            DashboardService().actualizar()
            st.success(
                "✅ Reporte registrado correctamente."
            )

            st.balloons()

            st.rerun()