from flask import Flask, jsonify, request
from flask_cors import CORS
from procesar_bibtext import BibTeXProcessor  # Importa la clase correctamente

app = Flask(__name__)
CORS(app)  # Habilita CORS si es necesario

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

# El servicio de Flask solo se inicia cuando ejecutas app.run
if __name__ == '__main__':
    app.run(debug=True)
