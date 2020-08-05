import xlrd
from datetime import datetime
import zipfile, os, sys

class ExcelToSQL:

    def __init__(self, filename):
        local_dir = '/home/dashere/Documentos/ArchivosUcen/Admision/'
        month = datetime.now().strftime('%b') + '/'
        self._path_parent = local_dir + month
        self._path_child = self._path_parent + filename + '/'
    
        with zipfile.ZipFile('/home/dashere/Descargas/' + filename + '.zip', 'r') as zip_ref:
            if os.path.isdir(self._path_child):
                zip_ref.extractall(self._path_child)
            elif os.path.isdir(self._path_parent):
                os.mkdir(self._path_child)
                zip_ref.extractall(self._path_child)
            else:
                os.mkdir(self._path_parent)
                os.mkdir(self._path_child)
                zip_ref.extractall(self._path_child)

        self._document = xlrd.open_workbook(self._path_child + filename + '.xlsx')
        self._sheet = self._document.sheet_by_index(0)

    def formatDataFromExcel(self):
        data, formated, cleaned = [], [], []
        # Sacar los datos de Excel
        for i in range(1, self._sheet.nrows):
            temp = [int(row.value) if isinstance(row.value, float) else str(row.value) for row in self._sheet.row(i)]
            data.append(temp)
        # Convertir fechas de Excel a string
        for row in data:
            if isinstance(row[2], int):
                row[2] = datetime.strftime(xlrd.xldate.xldate_as_datetime(row[2], self._document.datemode), '%Y-%m-%d')
            if isinstance(row[3], int):
                row[3] = datetime.strftime(xlrd.xldate.xldate_as_datetime(row[3], self._document.datemode), '%Y-%m-%d')

        # Formatear los datos
        new_index = [0,1,6,7,8,2,3,9,10,11,12,19,4,5,13,14,15,17,16,18]
        for row in data:
            new_order = [row[i] for i in new_index]
            formated.append(new_order)
        #return print(formated[1])
        for row in formated:
            row[18] = (int(row[16]) + int(row[17])) - (int(row[18]) + int(row[19]))
            row.pop(19)
            line = ''
            for i in range(0, len(row)):
                if row[i] == "NULL":
                    line += '\"\", '
                elif row[i] == "D'VORQUEZ":
                    line += '\"DVORQUEZ\", '
                elif isinstance(row[i], str):
                    line += '\"' + row[i] + '\", '
                elif isinstance(row[i], int):
                    line += str(row[i]) + ', '
            cleaned.append(line)
                
        return cleaned

    def to_sql(self):

        context = "INSERT INTO alumnos_admision ( rut_alumno, dv_alumno, nombres, paterno, materno, fecha_postulacion, fecha_matricula, codigo_programa, programa, sede, facultad, modalidad, anio, periodo, estado, correo_ucentral, arancel, matricula, descuento, id_oferta, id_sede, id_facultad, id_modalidad, id_periodo ) VALUES ("
        
        with open(self._path_child + "Admision_" + datetime.now().strftime('%d-%m-%Y') + ".sql", "w") as f:
            for line in self.formatDataFromExcel():
                f.write(context + line + "0, 0, 0, 0, 0);\n")



if __name__ == "__main__":

    convert = ExcelToSQL('SMARTCAMPUS_' + sys.argv[1])
    convert.to_sql()

