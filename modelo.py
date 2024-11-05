import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

# Cargamos el Data Frame con el origen o fuente de los datos (archivo CSV)
df = pd.read_csv('Dataset/data_recomienda.csv')

#Vectorizar la descripción para calcular similitud
#vectorizer = TfidfVectorizer()

# Mejorar el Preprocesamiento de Texto
# El preprocesamiento de los datos es clave cuando se trabaja con texto. Algunas sugerencias para mejorar la vectorización del contenido:
# Eliminar stopwords: Puedes eliminar palabras vacías (como "de", "y", "el", etc.) que no aportan información significativa. TfidfVectorizer permite incluir un parámetro stop_words='english' o incluso un conjunto de palabras personalizadas.
# lowercase=True indicaría que el texto debe ser convertido a minúsculas antes de continuar con el proceso.
# lowercase=False (o si no se especifica) indicaría que no se debe realizar la conversión y que el texto debe ser procesado tal como está.
vectorizer = TfidfVectorizer(stop_words='english', lowercase=True) # configuracion de TfidfVectorizery, en idioma ingles

tfidf_matrix = vectorizer.fit_transform(df['caracteristicas_pelicula'])
cosine_similarities = cosine_similarity(tfidf_matrix)

def recomendacion(titulo: str):
    # Buscar la película por título
    pelicula_index = df[df['title'].str.lower() == titulo.lower()].index

    if len(pelicula_index) == 0:
        return "No se encontró ninguna película con ese título."

    # Obtener el índice de la película
    idx = pelicula_index[0]

    # Obtener los puntajes de similitud para esa película
    sim_scores = list(enumerate(cosine_similarities[idx]))

    # Ordenar las películas basadas en la similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener las 5 películas más similares (excluyendo la misma)
    sim_scores = sim_scores[1:6]

    # Obtener los índices de las películas recomendadas
    movie_indices = [i[0] for i in sim_scores]

    # Devolver los títulos de las películas recomendadas
    return df['title'].iloc[movie_indices].tolist()


#Ejecutar el servidor FastAPI
#Puedes usar 'uvicorn nombre_del_archivo:app --reload' para ejecutar la API
