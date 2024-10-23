import bibtexparser
import pandas as pd
import os

class BibTeXProcessor:
    def __init__(self, carpeta):
        self.carpeta = carpeta

    def cargar_bibtex(self, ruta_archivo):
        """Carga un archivo BibTeX y lo devuelve como DataFrame."""
        with open(ruta_archivo, 'r', encoding='utf-8') as bib_file:  # Usar UTF-8 para leer el archivo
            bib_database = bibtexparser.load(bib_file)
        return pd.DataFrame(bib_database.entries)

    def combinar_archivos(self):
        """Combina todos los archivos .bib en la carpeta especificada."""
        archivos_bib = [f for f in os.listdir(self.carpeta) if f.endswith('.bib')]
        df_total = pd.DataFrame()  # Inicializar DataFrame vacío

        for archivo in archivos_bib:
            ruta_completa = os.path.join(self.carpeta, archivo)  # Obtener ruta completa
            df_parcial = self.cargar_bibtex(ruta_completa)
            df_total = pd.concat([df_total, df_parcial], ignore_index=True)

        return df_total

    def guardar_bibtex(self, df, archivo_salida):
        """Guarda el DataFrame en un archivo BibTeX."""
        db = bibtexparser.bibdatabase.BibDatabase()
        db.entries = df.to_dict('records')  # Convertir DataFrame a lista de diccionarios (formato de BibTeX)
        with open(archivo_salida, 'w', encoding='utf-8') as bib_file:  # Usar UTF-8 para escribir el archivo
            bibtexparser.dump(db, bib_file)

    def procesar(self, archivo_salida):
        """Método principal para combinar archivos y guardar el resultado."""
        df_total = self.combinar_archivos()

        # Convertir todos los campos a cadenas de texto
        df_total = df_total.astype(str)

        # Guardar el archivo combinado
        self.guardar_bibtex(df_total, archivo_salida)
        print(f"Archivo combinado guardado como '{archivo_salida}'")
