import pandas as pd
import bibtexparser

class GraficaAutoresMasCitados:
    def __init__(self, df):
        self.df = df

    # Método para obtener los 15 autores más citados
    def obtener_autores_mas_citados(self):
        # Excluir filas donde el autor es None, vacío o NaN
        self.df = self.df[self.df['author'].notna()]  # Excluir None
        self.df = self.df[self.df['author'] != ""]    # Excluir cadenas vacías
        self.df = self.df[self.df['author'] != "nan"] # Excluir 'nan' como string

        # Simulación: Usamos la longitud del DOI como aproximación de las citaciones
        self.df['citaciones'] = self.df['doi'].apply(lambda x: len(str(x)))  # Suponemos que la longitud del DOI es una métrica para las citas
        
        # Agrupamos las citaciones por autor
        citaciones_por_autor = self.df.groupby('author')['citaciones'].sum().nlargest(15).to_dict()

        return citaciones_por_autor
