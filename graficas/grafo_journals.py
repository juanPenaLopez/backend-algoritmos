import pandas as pd
import random
import networkx as nx
import matplotlib.pyplot as plt
import io

class GrafoJournals:

    def __init__(self, df):
        self.df = df

    # Obtener los 10 journals con más artículos publicados
    def obtener_journals_mas_publicados(self):
        return self.df.groupby('journal').size().nlargest(10)

    # Generar citaciones aleatorias entre 0 y 250
    def generar_citaciones_aleatorias(self):
        if 'citaciones' not in self.df.columns:
            self.df['citaciones'] = self.df['doi'].apply(lambda x: random.randint(0, 250))

    # Obtener los 15 artículos más citados por cada journal
    def obtener_articulos_mas_citados_por_journal(self, top_journals):
        articulos_por_journal = {}
        
        for journal in top_journals.index:
            articulos = self.df[self.df['journal'] == journal]
            top_articulos = articulos.nlargest(15, 'citaciones')
            articulos_por_journal[journal] = top_articulos
        
        return articulos_por_journal

    # Asignar países aleatorios al primer autor si falta el dato
    def asignar_paises_aleatorios(self):
        paises = ['USA', 'Canada', 'UK', 'Germany', 'Australia', 'France', 'Spain', 'Brazil', 'India', 'China']
        if 'pais_autor' not in self.df.columns:
            self.df['pais_autor'] = self.df['author'].apply(lambda x: random.choice(paises))

    # Crear el grafo de journals y artículos
    def crear_grafo(self, articulos_top_15):
        G = nx.Graph()

        for journal, articulos in articulos_top_15.items():
            G.add_node(journal, type='journal')
            
            for _, row in articulos.iterrows():
                articulo = row['title']
                G.add_node(articulo, type='articulo', citaciones=row['citaciones'])
                G.add_edge(journal, articulo)
                
                pais = row['pais_autor']
                G.add_node(pais, type='pais')
                G.add_edge(articulo, pais)
        
        return G

    # Función para generar y mostrar el grafo
    def generar_grafo(self):
        top_journals = self.obtener_journals_mas_publicados()
        self.generar_citaciones_aleatorias()
        self.asignar_paises_aleatorios()
        articulos_top_15 = self.obtener_articulos_mas_citados_por_journal(top_journals)
        G = self.crear_grafo(articulos_top_15)
        return G
