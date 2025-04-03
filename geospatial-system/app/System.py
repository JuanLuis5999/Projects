# This project uses original Spanish names for database tables, columns, and views 
# because it works with official datasets from INEGI (Mexico). 
# These names have been preserved to maintain consistency with the source structure.

from flask import Flask, request
import psycopg2
import webbrowser
from threading import Timer
app = Flask(__name__)
@app.route('/')
def formulario():
    return '''
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            form {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                max-width: 400px;
                width: 100%;
                text-align: center; /* Centrar el contenido dentro del formulario */
            }

            h1 {
                font-size: 24px; /* Cambia el tamaño de letra */
                font-weight: bold; /* Aplica negritas */
                margin-bottom: 20px;
            }

            img {
                max-width: 100%;
                height: auto;
                margin-bottom: 20px; /* Espacio entre la imagen y el título */
            }

            label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
            }

            input[type="text"],
            input[type="number"] {
                width: 100%;
                padding: 8px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }

            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                width: 100%;
            }

            button:hover {
                background-color: #45a049;
            }

            .form-group {
                margin-bottom: 15px;
            }
        </style>

        <form action="/procesar" method="POST" onsubmit="return validarFormulario()">
            <!-- Imagen como encabezado -->
            <img src="https://cdn.milenio.com/uploads/media/2014/03/06/instituto-federal-de-telecomunicaciones.jpeg" alt="Encabezado de la página">

            <!-- Título en negritas y con letra más grande -->
            <h1>Sistema de procesamiento y análisis de zonas de cobertura y áreas de servicio</h1>

            <div class="form-group">
                <label for="Columna">¿Qué valor quieres filtrar?:</label>
                <select name="Columna" id="Columna">
                    <option value="CANAL VIRTUAL ASIGNADO">Canal Virtual Asignado</option>
                    <option value="PROGRAMACIÓN">Canal de Programación</option>
                    <option value="CONCESIONARIO">Concesionario</option>
                    <option value="GRUPO">Grupo</option>
                    <option value="ESTADO">Estado</option>
                </select>
            </div>

            <div class="form-group">
                <label for="numero_decimal">Introduce el valor a buscar:</label>
                <input type="text" name="numero_decimal" id="numero_decimal">
            </div>

            <div class="form-group">
                <label for="respuesta">¿Deseas incluir Zonas de Cobertura o Áreas de Servicio?</label>
                <select name="respuesta" id="respuesta">
                    <option value="1">Solo Áreas de Servicio (AS)</option>
                    <option value="2">Solo Zonas de Cobertura (ZC)</option>
                </select>
            </div>

            <div class="form-group">
                <label for="estaciones">Equipos que se desean:</label>
                <select name="estaciones" id="estaciones">
                    <option value="PRINCIPAL">Principales (AS)</option>
                    <option value="COMPLEMENTARIA">Complementarias (ZC)</option>
                    <option value="PRINCIPAL,COMPLEMENTARIA">Principales y Complementarias (ZC)</option>
                </select>
            </div>

            <div class="form-group">
                <label for="estatus">Estatus:</label>
                <input type="text" name="estatus" id="estatus">
            </div>

            <button type="submit">Enviar</button>
        </form>
    '''


@app.route('/process', methods=['POST'])
def process():
    column = request.form['Columna']
    value = request.form['numero_decimal']
    response = int(request.form['respuesta'])
    stations = request.form['estaciones'].split(',')
    status = request.form['estatus'].split(',')

    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='.',
        dbname='postgres2',
        port=5433
    )

    cursor = connection.cursor()
    
    if column == 'CANAL VIRTUAL ASIGNADO':
        value = float(value)

    query_distinctive = f"""
        SELECT "DISTINTIVO"
        FROM "bd_multi"
        WHERE "{column}" = %s
    """
    cursor.execute(query_distinctive, (value,))
    distintivos = [f"{row[0]}-TDT" for row in cursor.fetchall()]
    print("Found distinctives:", distintivos)
    print("Count:", len(distintivos))

    stations_tuple = tuple(s.strip() for s in stations)
    status_tuple = tuple(s.strip() for s in status)

    query_service = """
        SELECT "NOMBRE_ARCHIVO_AS.SHP"
        FROM "bd_tdt"
        WHERE "DISTINTIVO-TDT" = ANY(%s)
        AND "BAJA_REGISTRO" = 1
        AND "TIPO_ESTACION" IN %s
        AND "ESTATUS" IN %s
    """

    query_coverage = """
        SELECT "NOMBRE_ARCHIVO_ZC"
        FROM "bd_tdt"
        WHERE "DISTINTIVO-TDT" = ANY(%s)
        AND "BAJA_REGISTRO" = 1
        AND "TIPO_ESTACION" IN %s
        AND "ESTATUS" IN %s
    """

    cursor.execute(query_service, (distintivos, stations_tuple, status_tuple))
    service_names = [row[0] for row in cursor.fetchall()]
    print("Service area station names found:", service_names)
    print("Count:", len(service_names))

    cursor.execute(query_coverage, (distintivos, stations_tuple, status_tuple))
    coverage_names = [row[0] for row in cursor.fetchall()]
    print("Coverage zone station names found:", coverage_names)
    print("Count:", len(coverage_names))

    view_service_query = """
        CREATE OR REPLACE VIEW vista AS
        SELECT * FROM areas_de_servicio WHERE archivo = ANY(%s)
    """

    view_coverage_query = """
        CREATE OR REPLACE VIEW vistazc AS
        SELECT * FROM zonas_de_cobertura WHERE name = ANY(%s)
    """

    if response == 1:
        cursor.execute(view_service_query, (service_names,))
    elif response == 2:
        cursor.execute(view_coverage_query, (coverage_names,))

    connection.commit()
    connection.close()

    print("View 'vista' created with filtered data.")
    return '''
        View created successfully.
        <script>
            setTimeout(function(){
                window.location.href = "/";
            }, 3000);
        </script>
    '''

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=False)
