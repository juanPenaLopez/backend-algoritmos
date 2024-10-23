import bibtexparser
import pandas as pd
import os

class UnificarBibtext:
    
    def __init__(self, archivos):
        self.archivos = archivos

    # Función para cargar un archivo BibTeX y devolverlo como DataFrame
    def cargar_bibtex(self, ruta_archivo):
        with open(ruta_archivo, 'r', encoding='utf-8') as bib_file:
            bib_database = bibtexparser.load(bib_file)
        return pd.DataFrame(bib_database.entries)

    # Convertir todos los campos a cadenas de texto, para evitar errores de tipo
    def convertir_a_cadena(self, df):
        for col in df.columns:
            df[col] = df[col].astype(str)  # Convertir todos los valores a cadena
        return df

    # Limpiar duplicados seleccionando el abstract más largo
    def limpiar_duplicados(self, df):
        # Agrupar por el título y quedarse con el abstract más largo
        df_cleaned = df.loc[df.groupby('title')['abstract'].idxmax()]
        return df_cleaned

    # Combinar archivos en uno solo con las columnas compartidas
    def combinar_bibtex(self):
        df_total = pd.DataFrame()  # DataFrame vacío para combinar todo

        for archivo in self.archivos:
            df_parcial = self.cargar_bibtex(archivo)

            # Selecciona solo las columnas compartidas o relevantes
            columnas_comunes = ['ENTRYTYPE', 'ID', 'abstract', 'author', 'title', 'year', 'doi', 'url', 'journal', 'issn', 'keywords', 'publisher', 'volume', 'pages']
            
            # Mantén solo las columnas que existan en el archivo
            columnas_existentes = [col for col in columnas_comunes if col in df_parcial.columns]
            df_parcial = df_parcial[columnas_existentes]
            
            # Convertir los valores a cadenas de texto
            df_parcial = self.convertir_a_cadena(df_parcial)
            
            # Unir al DataFrame total
            df_total = pd.concat([df_total, df_parcial], ignore_index=True)

        # Limpiar duplicados
        df_total = self.limpiar_duplicados(df_total)
        
        return df_total

    # Guardar el archivo BibTeX combinado
    def guardar_bibtex(self, df, ruta_archivo):
        db = bibtexparser.bibdatabase.BibDatabase()
        
        # Asegúrate de que cada entrada tenga 'ENTRYTYPE' y 'ID'
        for i, entry in df.iterrows():
            if 'ENTRYTYPE' not in entry or pd.isna(entry['ENTRYTYPE']):
                entry['ENTRYTYPE'] = 'article'  # Asignar un tipo por defecto si no existe
            if 'ID' not in entry or pd.isna(entry['ID']):
                entry['ID'] = f"entry_{i}"  # Generar un ID por defecto si no existe

        db.entries = df.to_dict('records')  # Convertir DataFrame a lista de diccionarios (formato de BibTeX)

        with open(ruta_archivo, 'w', encoding='utf-8') as bib_file:  # Guardar como UTF-8
            bibtexparser.dump(db, bib_file)

    # Ejecutar el proceso completo
    def procesar(self, archivo_salida):
        df_combined = self.combinar_bibtex()  # Combinar archivos
        self.guardar_bibtex(df_combined, archivo_salida)  # Guardar el archivo combinado
        print("Archivos combinados y limpiados exitosamente.")

# Usar la clase BibTeXProcessor
archivos = ['archivo2_completo.bib', 'archivo3_completo.bib', 'C:/Analisis-algoritmos/SCOPUS/scopus.bib']
processor = UnificarBibtext(archivos)
processor.procesar('archivo_combinado.bib')
