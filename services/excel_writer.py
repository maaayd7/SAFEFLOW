from pathlib import Path

from openpyxl import load_workbook


class ExcelWriter:

    def __init__(self):

        self.archivo = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "condiciones.xlsx"
        )

    print("ESTOY USANDO ESTE EXCEL_WRITER")
    def guardar_reporte(

        self,

        fecha,

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

        fecha_compromiso,

        foto=""

):

        wb = load_workbook(self.archivo)

        ws = wb.active

        fila = ws.max_row + 1

        numero = fila - 2

        ws.cell(fila, 1).value = numero
        ws.cell(fila, 2).value = fecha
        ws.cell(fila, 3).value = tipo
        ws.cell(fila, 4).value = descripcion
        ws.cell(fila, 5).value = consecuencia
        ws.cell(fila, 6).value = area
        ws.cell(fila, 7).value = lugar
        ws.cell(fila, 8).value = maquina
        ws.cell(fila, 9).value = reportado_por
        ws.cell(fila,10).value = responsable
        ws.cell(fila,11).value = prioridad
        ws.cell(fila,12).value = estado
        ws.cell(fila,13).value = fecha_compromiso
        ws.cell(fila,14).value = foto

        wb.save(self.archivo)

        wb.close()