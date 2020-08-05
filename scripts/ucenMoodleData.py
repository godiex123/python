from progress.bar import Bar
from time import sleep
from datetime import datetime, timedelta
from queries import actividades, materiales
import MySQLdb
import os, sys 

class MoodleDataSQL:

    def __init__(self):
        self._conn = MySQLdb.connect(host="192.168.100.26", user="smartcampus", passwd="uwt89B1dLvBsi7OJ", db="moodleaula202001")
        self._cursor = self._conn.cursor()

    def close(self):
        self._conn.close()

    def query(self, sql, params = None):
        self._cursor.execute(sql, params or ())

    def fetchall(self):
        return self._cursor.fetchall()

    def format_data(self):
        data = list()
        with Bar('Formateando', fill='#', suffix='%(percent).1f%% - %(eta)ds') as bar:
            for row in self.fetchall():
                line, top = '', len(row) - 1
                for i in range(0, len(row)):
                    if i == top:
                        if row[i] is not None:
                            if isinstance(row[i], str):
                                line += '\"' + row[i] + '\");'
                            else:
                                line += str(row[i]) + ');'
                        else:
                            line += '\"NULL\");'
                    else:
                        if row[i] is not None:
                            if isinstance(row[i], str):
                                line += '\"' + row[i] + '\", '
                            else:
                                line += str(row[i]) + ', '
                        else:
                            line += '\"NULL\", '
                data.append(line)
                sleep(0.02)
                bar.next()

        return data
                
    def download_to_sql(self, opt, filename, desde, hasta):

        if opt == 'act':

            context = "INSERT INTO actividad_aulas(idnumber, facultad, escuela, programa, curso, seccion_curso, inicio, nombre_docentes, cantidad_docentes, docentes_activos, hits_total_cu_docentes, radio_10_docente, hits_periodo_cu_docentes, estudiantes, estudiantes_activos, hits_total_estudiantes, radio_10_estudiante, hits_periodo_estudiantes, curso_activo, fecha_registro) VALUES ("

            self.query(actividades, {'registro':sys.argv[2], 'desde':desde, 'hasta':hasta})
        
        else:

            context = "INSERT INTO material_aulas(idnumber, facultad, escuela, programa, curso, seccion_curso, creacion, inicio, nombre_docentes, cantidad_docentes, tot_recursos, tot_actividades, otros_recursos, otros_actividades, cuestionarios, encuestas, talleres, tareas, archivos_recursos, url, archivos, video_conferencias, fecha_registro) VALUES ("

            self.query(materiales, {'desde':desde, 'hasta':hasta})
        
        with open('/home/dashere/Descargas/' + filename, 'w') as f:
            with Bar('Escribiendo', fill='#', suffix='%(percent).1f%% - %(eta)ds') as bar:
                for line in self.format_data():
                    f.write(context + line + '\n')
                    sleep(0.02)
                    bar.next()

        if os.path.exists('/home/dashere/Descargas/' + filename):
            print("Archivo SQL Generado!")
        else:
            print("Error en la descarga del archivo!")


if __name__ == "__main__":

    print("Iniciando proceso de descarga SQL...")
    conexion = MoodleDataSQL()

    if sys.argv[1] == 'actividades': 
        desde = datetime.strftime(datetime.combine(datetime.strptime(sys.argv[2], '%Y-%m-%d'), datetime.min.time()), '%Y-%m-%d %H:%M:%S')
        hasta = datetime.strftime(datetime.strptime(desde, '%Y-%m-%d %H:%M:%S') + timedelta(days=1),'%Y-%m-%d %H:%M:%S')
        conexion.download_to_sql('act', 'Actividades_' + sys.argv[2] + '.sql', desde, hasta)

    elif sys.argv[1] == 'materiales':
        desde = sys.argv[2]
        hasta = datetime.strftime(datetime.strptime(desde, '%Y-%m-%d') + timedelta(days=1),'%Y-%m-%d')
        conexion.download_to_sql('mat', 'Materiales_' + desde + '.sql', desde, hasta)

    else:
        print("Opcion no reconocida. [actividades] o [materiales] disponibles")

    conexion.close()

        