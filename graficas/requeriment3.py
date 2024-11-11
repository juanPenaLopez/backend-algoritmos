import nltk
import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import wordnet as wn

# Descargar WordNet si aún no lo has hecho
nltk.download('wordnet')
nltk.download('omw-1.4')

class FrecuenciaAparicion:

    def __init__(self, df):
        self.df = df
        self.habilidades = ['Abstraction', 'Algorithm', 'Algorithmic thinking', 'Coding', 'Collaboration', 'Cooperation', 'Creativity', 'Critical thinking', 'Debug', 'Decomposition', 'Evaluation', 'Generalization', 'Logic', 'Logical thinking', 'Modularity', 'Patterns recognition', 'Problem solving', 'Programming', 'Representation', 'Reuse', 'Simulation']
        self.conceptos_computacionales = ['Conditionals', 'Control structures', 'Directions', 'Events', 'Functions', 'Loops', 'Modular structure', 'Parallelism', 'Sequences', 'Software/hardware', 'Variables']

        # Crear los diccionarios de sinónimos para habilidades y conceptos
        self.synonyms_habilidades = self.build_synonym_dict(self.habilidades)
        self.synonyms_conceptos = self.build_synonym_dict(self.conceptos_computacionales)

        # Aplicar limpieza y unificación de sinónimos a los resúmenes (abstracts)
        self.df['cleaned_abstract'] = self.df['abstract'].apply(self.clean_text)
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_habilidades))
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_conceptos))

    # Función para limpiar el texto (lowercase y eliminar caracteres especiales)
    def clean_text(self, text):
        text = text.lower()  # Convertir a minúsculas
        text = re.sub(r'\W+', ' ', text)  # Eliminar caracteres especiales
        return text

    # Función para obtener sinónimos usando WordNet
    def get_synonyms(self, word):
        synonyms = set()
        for synset in wn.synsets(word):
            for lemma in synset.lemmas():
                synonyms.add(lemma.name().lower())  # Añadir sinónimos en minúsculas
        return synonyms

    # Construir el diccionario de sinónimos
    def build_synonym_dict(self, palabras_clave):
        synonym_dict = {}
        for word in palabras_clave:
            synonyms = self.get_synonyms(word)  # Obtener sinónimos
            for synonym in synonyms:
                synonym_dict[synonym] = word.lower()  # Mapear sinónimos a la palabra clave original
        return synonym_dict

    # Función para unificar sinónimos en el texto
    def unify_synonyms(self, text, synonym_dict):
        words = text.split()
        unified_words = [synonym_dict.get(word, word) for word in words]  # Reemplazar sinónimos por la palabra clave
        return ' '.join(unified_words)

    # Función para contar frecuencias en una categoría
    def contar_frecuencias(self, palabras_clave, categoria):
        rows = []
        for palabra in palabras_clave:
            cantidad = self.df['cleaned_abstract'].str.count(palabra.lower()).sum()
            if cantidad > 0:
                rows.append({'término': palabra, 'categoría': categoria, 'cantidad': cantidad})
        return pd.DataFrame(rows)

    # Función para obtener las frecuencias de todas las categorías
    def obtener_frecuencias(self):
        df_habilidades = self.contar_frecuencias(self.habilidades, "Habilidades")
        df_conceptos = self.contar_frecuencias(self.conceptos_computacionales, "Conceptos Computacionales")
        # Combinar todas las categorías en un solo DataFrame
        df_frecuencias = pd.concat([df_habilidades, df_conceptos], ignore_index=True)
        return df_frecuencias

    # Crear una pivot_table que agrupe los términos por categoría
    def crear_pivot_table(self, df_frecuencias):
        pivot_table = pd.pivot_table(df_frecuencias, values='cantidad', index='término', columns='categoría', aggfunc='sum', fill_value=0)
        return pivot_table

    # Función para graficar la pivot_table
    def graficar_pivot_table(self, pivot_table):
        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot_table, annot=True, cmap="Blues", cbar=True)
        plt.title('Frecuencia de términos por categoría')
        plt.xlabel('Categoría')
        plt.ylabel('Término')
        plt.show()

# Uso de la clase

# Cargar tus datos en un DataFrame (ejemplo)
# df = pd.read_csv('tu_archivo.csv')

# Instanciar la clase con el DataFrame
# fa = FrecuenciaAparicion(df)

# Obtener las frecuencias de habilidades y conceptos computacionales
# df_frecuencias = fa.obtener_frecuencias()

# Crear la tabla pivot
# pivot_table = fa.crear_pivot_table(df_frecuencias)

# Graficar la tabla pivot
# fa.graficar_pivot_table(pivot_table)
