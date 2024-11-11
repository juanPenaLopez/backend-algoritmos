from io import BytesIO
from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS
from procesar_bibtext import BibTeXProcessor  # Importa la clase correctamente
import bibtexparser
from pandas import pandas as pd
from graficas.grafica1 import GraficaAutoresMasCitados
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.io as pio
import io
import base64
from graficas.grafo_journals import GrafoJournals
import networkx as nx
from graficas.requeriment3 import FrecuenciaAparicion

app = Flask(__name__)
CORS(app)  # Habilita CORS si es necesario

# Variable global para almacenar el DataFrame cargado
df_global = None

@app.route('/', methods=['GET'])
def home1():
    return render_template('base.html')

@app.route('/api', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Flask backend!"})

# Ruta para procesar archivos BibTeX, solo se ejecuta al hacer la petición POST
@app.route('/process_bibtex', methods=['POST'])
def process_bibtex():
    # Obtener los datos de la solicitud JSON
    data = request.get_json()
    
    # Obtener la ruta de la carpeta y el archivo de salida
    carpeta = data.get('carpeta')
    archivo_salida = data.get('archivo_salida')

    # Validación de parámetros
    if not carpeta or not archivo_salida:
        return jsonify({"error": "Faltan los parámetros 'carpeta' y 'archivo_salida'"}), 400

    try:
        # Crear una instancia de BibTeXProcessor con la carpeta proporcionada
        processor = BibTeXProcessor(carpeta)

        # Ejecutar la lógica de combinación de BibTeX
        processor.procesar(archivo_salida)

        return jsonify({"message": f"Archivo combinado guardado como '{archivo_salida}'"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Función para leer el archivo .bib y convertirlo en un DataFrame
def cargar_datos_bibtex(archivo):
    try:
        # Abrir el archivo con la codificación 'utf-8'
        with open(archivo, encoding='utf-8') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        entries = bib_database.entries
        df = pd.DataFrame(entries)
        print("Archivo .bib cargado exitosamente.")
        return df
    except Exception as e:
        print(f"Error al cargar el archivo .bib: {str(e)}")
        return None

@app.route('/autores_mas_citados', methods=['GET'])
def autores_mas_citados():
    if df_global is not None:
        # Creamos la instancia de la clase GraficaAutoresMasCitados con el DataFrame cargado
        grafica_service = GraficaAutoresMasCitados(df_global)
        
        # Obtenemos los 15 autores más citados
        autores = grafica_service.obtener_autores_mas_citados()

        # Generar la gráfica de barras horizontales
        autores_list = list(autores.keys())
        citaciones_list = list(autores.values())
        
        plt.figure(figsize=(10, 6))  # Ajustamos el tamaño de la figura
        plt.barh(autores_list, citaciones_list, color='skyblue')
        plt.xlabel('Cantidad de Citaciones')
        plt.ylabel('Autores')
        plt.title('Top 15 Autores Más Citados')

        # Guardamos la gráfica en un objeto de tipo bytes
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='png')
        img_stream.seek(0)  # Retrocedemos al inicio del archivo en memoria
        img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')

        # Cerramos la gráfica para liberar recursos
        plt.close()

        # Retornamos la gráfica en base64 junto con los datos en JSON
        return jsonify({
            "autores_mas_citados": autores,
            "grafica": img_base64
        }), 200
    else:
        return jsonify({"error": "Error al cargar los datos del archivo .bib"}), 500

@app.route('/grafica/articulos_por_ano', methods=['GET'])
def grafica_articulos_por_ano():
    if df_global is not None:
        # Generar gráfico interactivo
        grafico_html = generar_grafico_productos_por_ano(df_global)
        return grafico_html
    else:
        return jsonify({"error": "Error al cargar el archivo .bib"}), 500

# Función para contar productos por año
def contar_productos_por_ano(df):
    if 'year' in df.columns:
        # Convertir columna 'year' a numérico
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        # Contar productos por año
        conteo_ano = df['year'].value_counts().sort_index()
        return conteo_ano
    else:
        return pd.Series()

# Función para generar gráfico interactivo con Plotly
def generar_grafico_productos_por_ano(df):
    conteo_ano = contar_productos_por_ano(df)

    # Crear la figura de barras
    fig = go.Figure(data=[go.Bar(
        x=conteo_ano.index,
        y=conteo_ano.values,
        text=conteo_ano.values,  # Añadir la cantidad como texto
        hoverinfo='x+text',  # Información al pasar el cursor (x = año, text = cantidad)
        marker=dict(color='skyblue')
    )])

    # Configuraciones de la gráfica
    fig.update_layout(
        title='Cantidad de Productos por Año',
        xaxis_title='Año',
        yaxis_title='Cantidad de Productos',
        template='plotly_white'
    )

    # Convertir la figura a HTML para mostrar en la web
    return pio.to_html(fig, full_html=False)

# Ejecutamos la inicialización cuando arranca el servidor
def inicializar_datos():
    global df_global
    df_global = cargar_datos_bibtex('archivo_combinado.bib')

@app.route('/grafica/tipo-productos', methods=['GET'])
def obtener_tipo_producto():
    if df_global is not None:
        # Contamos los tipos de productos (artículos, conferencias, etc.)
        tipos_productos = df_global['type'].value_counts()

        # Crear gráfico de pastel
        fig, ax = plt.subplots()
        ax.pie(tipos_productos, labels=tipos_productos.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax.axis('equal')  # Para que el gráfico de pastel sea un círculo perfecto
        
        # Guardar el gráfico en un objeto BytesIO
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)  # Mover al principio del archivo
        
        # Retornar el gráfico como imagen en respuesta
        return send_file(img, mimetype='image/png', as_attachment=False)
    else:
        return jsonify({"error": "Error al cargar los datos del archivo .bib"}), 500

@app.route('/grafica-journals', methods=['GET'])
def obtener_journals_mas_frecuentes():
    if df_global is not None:
        # Contamos la cantidad de veces que aparece cada journal
        conteo_journals = df_global['journal'].value_counts().nlargest(15)  # Obtener los 15 más frecuentes
        
        # Crear gráfico de barras horizontales
        fig, ax = plt.subplots(figsize=(10, 6))
        conteo_journals.plot(kind='barh', color='skyblue', ax=ax)
        ax.set_xlabel('Cantidad de apariciones')
        ax.set_ylabel('Journals')
        ax.set_title('Top 15 Journals más frecuentes')
        
        # Guardar el gráfico en un objeto BytesIO
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)  # Mover al principio del archivo
        
        # Retornar el gráfico como imagen en respuesta
        return send_file(img, mimetype='image/png', as_attachment=False)
    else:
        return jsonify({"error": "Error al cargar los datos del archivo .bib"}), 500

# Instancia de la clase GrafoJournals
grafo_service = GrafoJournals(df_global)

# Instancia de la clase FrecuenciaAparicion
frecuencia_aparicion = FrecuenciaAparicion(df_global)

@app.route('/frecuencia-apariciones', methods=['GET'])
def mostrar_frecuencia_apariciones():

    # Obtener frecuencias
    df_frecuencias = frecuencia_aparicion.obtener_frecuencias()

    # Crear la tabla pivot
    pivot_table = frecuencia_aparicion.crear_pivot_table(df_frecuencias)

    # Graficar la tabla pivot
    frecuencia_aparicion.graficar_pivot_table(pivot_table)
    
    # Guardar el grafo en un buffer de memoria y enviarlo como archivo de imagen
    img = io.BytesIO()
    plt.savefig(img, format='PNG')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

@app.route('/grafo_journals')
def mostrar_grafo_journals():
    # Generar el grafo
    G = grafo_service.generar_grafo()

    # Dibujar el grafo
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
    
    # Guardar el grafo en un buffer de memoria y enviarlo como archivo de imagen
    img = io.BytesIO()
    plt.savefig(img, format='PNG')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    # Cargar los datos antes de iniciar el servidor
    inicializar_datos()

    # Iniciar el servidor Flask
    app.run(debug=True)
