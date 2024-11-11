import nltk
import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import wordnet as wn
import io

# Descargar WordNet si aún no lo has hecho
nltk.download('wordnet')
nltk.download('omw-1.4')

class FrecuenciaAparicion:

    def __init__(self, df):
        self.df = df
        self.habilidades = ['Abstraction', 'Algorithm', 'Algorithmic thinking', 'Coding', 'Collaboration', 'Cooperation', 'Creativity', 'Critical thinking', 'Debug', 'Decomposition', 'Evaluation', 'Generalization', 'Logic', 'Logical thinking', 'Modularity', 'Patterns recognition', 'Problem solving', 'Programming', 'Representation', 'Reuse', 'Simulation']
        self.conceptos_computacionales = ['Conditionals', 'Control structures', 'Directions', 'Events', 'Functions', 'Loops', 'Modular structure', 'Parallelism', 'Sequences', 'Software/hardware', 'Variables']
        self.actitudes = ['emotional', 'engagement', 'motivation', 'perceptions', 'persistence', 'self efficacy', 'self perceived']
        self.propiedad_psicometricas = ['classical test theory', 'confirmatory factor analysis', 'exploratory factor analysis', 'item response theory', 'reliability', 'structural equation model', 'validity']
        self.herramienta_evaluacion = ['bctt', 'escas', 'cctt', 'ctst', 'cta-ces', 'ctc', 'ctls', 'cts', 'ctt-es', 'ctt-lp', 'capct', 'ict', 'competency test', 'self-efficacy scale', 'stem las']
        self.diseno_investigacion = ['experimental', 'longitudinal research', 'mixed methods', 'post-test', 'pre-test', 'quasi-experiments', 'no experimental']
        self.nivel_escolaridad = ['upper elementary education', 'primary school', 'early childhood education', 'secondary school', 'high school', 'university', 'college']
        self.medio = ['block programming', 'mobile application', 'pair programming', 'plugged activities', 'programming', 'robotics', 'spreadsheet', 'stem', 'unplugged activities']
        self.estrategia = ['construct-by-self mind mapping', 'design-based learning', 'gamification', 'reverse engineering', 'technology-enhanced learning', 'collaborative learning', 'cooperative learning', 'flipped classroom', 'game-based learning', 'inquiry-based learning', 'personalized learning', 'problem-based learning', 'project-based learning', 'universal design for learning']
        self.herramienta = ['alice', 'arduino', 'scratch', 'scratchJr', 'blockly Games', 'code.org', 'codecombat', 'CSUnplugged', 'Robot Turtles', 'Hello Ruby', 'Kodable', 'LightbotJr', 'KIBO robots', 'BEE BOT', 'CUBETTO', 'Minecraft', 'Agent Sheets', 'Mimo', 'Py–Learn', 'SpaceChem']

        # Crear los diccionarios de sinónimos para habilidades y conceptos
        self.synonyms_habilidades = self.build_synonym_dict(self.habilidades)
        self.synonyms_conceptos = self.build_synonym_dict(self.conceptos_computacionales)
        self.synonyms_actitudes = self.build_synonym_dict(self.actitudes)
        self.synonyms_propiedad_psicometrica = self.build_synonym_dict(self.propiedad_psicometricas)
        self.synonyms_herramienta_evaluacion = self.build_synonym_dict(self.herramienta_evaluacion)
        self.synonyms_diseno_investigacion = self.build_synonym_dict(self.diseno_investigacion)
        self.synonyms_nivel_escolaridad = self.build_synonym_dict(self.nivel_escolaridad)
        self.synonyms_medio = self.build_synonym_dict(self.medio)
        self.synonyms_estrategia = self.build_synonym_dict(self.estrategia)
        self.synonyms_herramienta = self.build_synonym_dict(self.herramienta)

        # Aplicar limpieza y unificación de sinónimos a los resúmenes (abstracts)
        self.df['cleaned_abstract'] = self.df['abstract'].apply(self.clean_text)
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_habilidades))
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_conceptos))
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_actitudes))
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_propiedad_psicometrica))
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_herramienta_evaluacion))
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_diseno_investigacion))
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_nivel_escolaridad))
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_medio))
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_estrategia))
        self.df['cleaned_abstract'] = self.df['cleaned_abstract'].apply(lambda x: self.unify_synonyms(x, self.synonyms_herramienta))

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
        df_actitudes = self.contar_frecuencias(self.actitudes, "Actitudes")
        df_propiedad = self.contar_frecuencias(self.propiedad_psicometricas, "Propiedades psicométricas")
        df_herramienta = self.contar_frecuencias(self.herramienta_evaluacion, "Herramienta de evaluación")
        df_diseno = self.contar_frecuencias(self.diseno_investigacion, "Diseño de investigación")
        df_nivel = self.contar_frecuencias(self.nivel_escolaridad, "Nivel de escolaridad")
        df_medio = self.contar_frecuencias(self.medio, "Medio")
        df_estrategia = self.contar_frecuencias(self.estrategia, "Estrategia")
        df_herramientas = self.contar_frecuencias(self.herramienta, "Herramienta")

        # Combinar todas las categorías en un solo DataFrame
        df_frecuencias = pd.concat([df_habilidades, df_conceptos, df_actitudes, df_propiedad,
                                    df_herramienta, df_diseno, df_nivel, df_medio, df_estrategia,
                                    df_herramientas], ignore_index=True)
        return df_frecuencias

    # Crear una pivot_table que agrupe los términos por categoría
    def crear_pivot_table(self, df_frecuencias):
        pivot_table = pd.pivot_table(df_frecuencias, values='cantidad', index='término', columns='categoría', aggfunc='sum', fill_value=0)
        return pivot_table

    # Función para graficar la pivot_table
    def graficar_pivot_table(self, pivot_table):
        # Crear la figura
        plt.figure(figsize=(14, 10))  # Ajustar el tamaño según los datos
        sns.heatmap(pivot_table, annot=True, cmap="Blues", cbar=True)
        plt.title('Frecuencia de términos por categoría')
        plt.xlabel('Categoría')
        plt.ylabel('Término')
        
        # Guardar el gráfico en un buffer de memoria
        img = io.BytesIO()
        plt.savefig(img, format='PNG', bbox_inches='tight')  # Ajuste para que se recorte bien la imagen
        img.seek(0)  # Volver al principio del buffer
        plt.close()  # Cerrar la figura para liberar recursos

        return img  # Devolver el archivo de imagen en memoria
