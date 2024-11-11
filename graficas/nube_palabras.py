import pandas as pd
from collections import defaultdict
import re
import string
import nltk
from nltk.corpus import wordnet
from tqdm import tqdm
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class NubePalabras:
    def __init__(self, df):
        self.df = df 
        print("Descargando WordNet...")
        nltk.download("wordnet", quiet=True)

        self.categories_keywords = {
            "Habilidades": [
        "abstraction",
        "algorithm",
        "algorithmic thinking",
        "coding",
        "collaboration",
        "cooperation",
        "creativity",
        "critical thinking",
        "debug",
        "decomposition",
        "evaluation",
        "generalization",
        "logic",
        "logical thinking",
        "modularity",
        "pattern recognition",
        "problem solving",
        "programming",
        "representation",
        "reuse",
        "simulation",
    ],
    "Conceptos Computacionales": [
        "conditionals",
        "control structures",
        "directions",
        "events",
        "functions",
        "loops",
        "modular structure",
        "parallelism",
        "sequences",
        "software",
        "hardware",
        "variables",
    ],
    "Actitudes": [
        "emotional",
        "engagement",
        "motivation",
        "perceptions",
        "persistence",
        "self efficacy",
        "self perceived",
    ],
    "Propiedades Psicométricas": [
        "classical test theory",
        "confirmatory factor analysis",
        "exploratory factor analysis",
        "item response theory",
        "reliability",
        "structural equation model",
        "validity",
    ],
    "Herramienta de Evaluación": [
        "bctt",
        "escas",
        "cctt",
        "ctst",
        "cta-ces",
        "ctc",
        "ctls",
        "cts",
        "ctt-es",
        "ctt-lp",
        "capct",
        "ict",
        "competency test",
        "self-efficacy scale",
        "stem las",
    ],
    "Diseño de Investigación": [
        "experimental",
        "longitudinal research",
        "mixed methods",
        "post-test",
        "pre-test",
        "quasi-experiments",
        "no experimental",
    ],
    "Nivel de Escolaridad": [
        "upper elementary education",
        "primary school",
        "early childhood education",
        "secondary school",
        "high school",
        "university",
        "college",
    ],
    "Medio": [
        "block programming",
        "mobile application",
        "pair programming",
        "plugged activities",
        "programming",
        "robotics",
        "spreadsheet",
        "stem",
        "unplugged activities",
    ],
    "Estrategia": [
        "construct-by-self mind mapping",
        "design-based learning",
        "gamification",
        "reverse engineering",
        "technology-enhanced learning",
        "collaborative learning",
        "cooperative learning",
        "flipped classroom",
        "game-based learning",
        "inquiry-based learning",
        "personalized learning",
        "problem-based learning",
        "project-based learning",
        "universal design for learning",
    ],
    "Herramienta": [
        "alice",
        "arduino",
        "scratch",
        "scratchJr",
        "blockly Games",
        "code.org",
        "codecombat",
        "CSUnplugged",
        "Robot Turtles",
        "Hello Ruby",
        "Kodable",
        "LightbotJr",
        "KIBO robots",
        "BEE BOT",
        "CUBETTO",
        "Minecraft",
        "Agent Sheets",
        "Mimo",
        "Py–Learn",
        "SpaceChem",]
        }
        self.expanded_categories_keywords = self.expand_keywords()

    def obtener_sinonimos(self, palabra):
        sinonimos = set()
        if " " in palabra:
            return [palabra]
        for syn in wordnet.synsets(palabra):
            for lemma in syn.lemmas():
                if lemma.name().lower() != palabra.lower():
                    sinonimos.add(lemma.name().lower())
        return list(sinonimos)

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(f"[{string.punctuation}]", " ", text)
        text = re.sub(r"\d+", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def expand_keywords(self):
        expanded_keywords = {}
        for categoria, palabras in self.categories_keywords.items():
            expanded_palabras = []
            for palabra in palabras:
                expanded_palabras.append(palabra)
                sinonimos = self.obtener_sinonimos(palabra)
                expanded_palabras.extend(sinonimos)
            expanded_keywords[categoria] = expanded_palabras
        return expanded_keywords

    def contar_frecuencias(self):
        category_counts = defaultdict(int)
        for abstract in tqdm(self.df["abstract"].dropna()):
            abstract_cleaned = self.clean_text(abstract)
            for keywords_list in self.expanded_categories_keywords.values():
                for term in keywords_list:
                    term_pattern = r"\b" + re.escape(term.lower()) + r"\b"
                    term_count = len(re.findall(term_pattern, abstract_cleaned))
                    if term_count > 0:
                        category_counts[term] += term_count
        return category_counts

    def generar_nube_palabras(self, frecuencia_palabras):
        nube_palabras = WordCloud(width=800, height=400, background_color="white", max_words=100)
        nube_palabras.generate_from_frequencies(frecuencia_palabras)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(nube_palabras, interpolation="bilinear")
        plt.axis("off")
        plt.show()
