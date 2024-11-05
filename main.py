from fastapi import FastAPI, Response, HTTPException
import pandas as pd
from datetime import datetime
import numpy as np
import uvicorn
from unidecode import unidecode

import modelo as ml # importamos el modelo
import modelo3 as ml3 # probaremos este otro

app = FastAPI()

if __name__ == "__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Leer el archivo Parquet
# df = pd.read_parquet('data.parquet')  # Asegúrate de que el archivo esté en el mismo directorio o proporciona la ruta correcta
# df['release_date'] 

df = pd.read_csv('data.csv')
#print(df['release_date'])
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['release_year'] = df['release_date'].dt.year  # Extraer el año de la fecha

features = df[['release_date']].fillna(0)  # Rellena valores nulos


# Funcion 1
# # Función para contar películas por mes
# Función para contar películas por mes
def cantidad_filmaciones_mes(mes: str):
    # Diccionario de meses en español
    meses_dict = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }

    mes = mes.lower()  # Convertir a minúsculas para facilitar la comparación
    mes_num = meses_dict.get(mes)

    if mes_num is None:
        return "Mes inválido. Por favor ingrese un mes en español."

    # Contar las películas estrenadas en ese mes
    cantidad = df[df['release_date'].dt.month == mes_num].shape[0]

    return f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}"

# endpoints 
@app.get("/cantidad_filmaciones_mes/{mes}")
async def obtener_cantidad_filmaciones_mes(mes: str):
    return cantidad_filmaciones_mes(mes)


# Funcion 2
# Función para contar películas por día de la semana
def cantidad_filmaciones_dia(dia: str):
    # Diccionario de días en español
    dias_dict = {
        'lunes': 0, 'martes': 1, 'miercoles': 2, 'jueves': 3,
        'viernes': 4, 'sabado': 5, 'domingo': 6
    }

    #dia = dia.lower()  # Convertir a minúsculas para facilitar la comparación
    dia = unidecode(dia.lower()) # Eliminar acentos y convertir a minúsculas
    dia_num = dias_dict.get(dia)

    if dia_num is None:
        return "Día inválido. Por favor ingrese un día de la semana en español."

    # Contar las películas estrenadas en ese día de la semana
    cantidad = df[df['release_date'].dt.dayofweek == dia_num].shape[0]

    return f"{cantidad} películas fueron estrenadas en {dia.capitalize()}"

@app.get("/cantidad_filmaciones_dia/{dia}")
async def obtener_cantidad_filmaciones_dia(dia: str):
    return cantidad_filmaciones_dia(dia)


# Funcion 3
# Función para obtener información sobre la película
# Función para obtener información sobre la película
def score_titulo(titulo_de_la_filmacion: str):
    # Diccionarios para formatear la salida del mensaje al usuario
    dict_meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }

    dict_dias = {
        0: 'lunes', 1: 'martes', 2: 'miércoles', 3: 'jueves',
        4: 'viernes', 5: 'sábado', 6: 'domingo'
    }
    
    # Buscar la película por título
    pelicula = df[df['title'].str.lower() == titulo_de_la_filmacion.lower()]

    if pelicula.empty:
        return "No se encontró ninguna película con ese título."

    # Extraer información
    titulo = pelicula['title'].values[0]
    año = pelicula['release_year'].values[0]
    score = pelicula['popularity'].values[0]
    mes = pelicula['release_date'].dt.month.values[0]  # Obtener el mes
    
    # Obtener el día y el nombre del mes
    dia_numero = pelicula['release_date'].dt.weekday.values[0]  # Obtener el número del día
    nombre_mes = dict_meses.get(mes)
    nombre_dia = dict_dias.get(dia_numero)
    
    return f"La película '{titulo}' fue estrenada el día {nombre_dia} de {nombre_mes} del año {año} con una popularidad de: {score}."

@app.get("/score_titulo/{titulo_de_la_filmacion}")
async def obtener_score_titulo(titulo_de_la_filmacion: str):
    return score_titulo(titulo_de_la_filmacion)



# Funcion 4

def votos_titulo(titulo_de_la_filmación: str):
    # Buscar la película por título
    pelicula = df[df['title'].str.lower() == titulo_de_la_filmación.lower()]

    if pelicula.empty:
        return "No se encontró ninguna película con ese título.", 404

    # Extraer información
    titulo = pelicula['title'].values[0]
    año = pelicula['release_year'].values[0]
    cantidad_votaciones = pelicula['vote_count'].values[0]
    promedio_votaciones = pelicula['vote_average'].values[0]
    
    # Verificar si tiene al menos 2000 valoraciones
    if cantidad_votaciones < 2000:
        return "La película no cumple con el requisito de al menos 2000 valoraciones.", 400
    
    return (f"La película '{titulo}' fue estrenada en el año {año}. "
            f"La misma cuenta con un total de {cantidad_votaciones} valoraciones, "
            f"con un promedio de {promedio_votaciones:.2f}.", 200)

@app.get("/votos_titulo/{titulo_de_la_filmacion}")
async def obtener_votos_titulo(titulo_de_la_filmacion: str):
    resultado, status_code = votos_titulo(titulo_de_la_filmacion)
    return Response(content=resultado, media_type="text/plain", status_code=status_code)


# Funcion 7 Modelo de recomendacion

@app.get("/recomendacion/{titulo}")
async def obtener_recomendacion(titulo: str):
    resultado = ml3.recomendacion(titulo)
    if isinstance(resultado, str):
        raise HTTPException(status_code=404, detail=resultado)
    return Response(content=", ".join(resultado), media_type="text/plain")