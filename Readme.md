 
# PROYECTO INDIVIDUAL

## Temática: Plataforma de streaming

### Sistema de Recomendación API – Render

Proyecto de ciencia de datos y modelo de recomendación para una fuente de información en formato de texto CSV con columnas. Por lo tanto, se deben aplicar las técnicas necesarias para procesar la información y mejorar la calidad de los datos en primera instancia.

Para esto, es necesario realizar el proceso de **ETL** (Extracción, Transformación y Carga), en el cual se lleva a cabo una comprensión estructural y de la información de los datos. Después de ello, sigue el **EDA** (Análisis Exploratorio de Datos), donde se realiza un análisis de la información luego de ser transformada y depurada.

El proyecto requiere la creación de **APIs** para ser consultadas por los usuarios. Cada una de ellas responderá a una función específica de acuerdo a lo estipulado en la guía de desarrollo, desplegada en el **Web Service de Render**.

---

## Origen de los Datos

Los archivos de datos se encuentran en formato **CSV**. El primero de ellos, llamado `movies_dataset`, contiene **45,466 registros** y **22 columnas** con información diversa que caracteriza cada película. El segundo archivo de datos, llamado `credits`, tiene **45,504 registros** y **3 columnas**, y entre sus datos anidados tipo lista de diccionarios se encuentra información sobre los directores y actores de las películas.

---

## Limpieza y Transformación de los Datos (ETL)

En este proceso se analizó la estructura de los datos y su contenido de manera minuciosa, encontrando variedad de tipos de datos, incluyendo campos que denotan diccionarios de datos o listas de diccionarios.

De acuerdo con los requerimientos del proyecto, se abordaron los siguientes pasos:

1. **Eliminación de columnas irrelevantes**: Se eliminaron las columnas que no tienen incidencia en la solicitud de este proyecto.
2. **Depuración de datos nulos**: Se listaron las cantidades de datos nulos por cada campo, y se procedió a depurarlos hasta lograr que ningún campo contenga valores nulos.
3. **Tratamiento de duplicados**: Se eliminaron los registros duplicados en relación con el campo `title`, ya que este es un campo clave para el modelo de recomendación.
4. **Imputación de valores numéricos**: Los valores numéricos nulos fueron reemplazados por ceros.
5. **Formateo de datos**: Se aseguraron de que los datos estuvieran correctamente formateados (por ejemplo, `date`, `float`, `int`, etc.).
6. **Extracción de información de diccionarios**: Se creó una función que extrae el valor de la clave `name` de cada diccionario en la lista, y con estos valores se llenaron nuevos campos en el conjunto de datos.

### Restricciones

Render, en su opción gratuita, permite servicios web con un tamaño máximo de 512 MB. Esto obliga a utilizar formatos de compresión de datos o recorte de los archivos procesados para ajustarse a esta limitación.

---

## Análisis Exploratorio de los Datos (EDA)

Durante este análisis, se observaron varias características de las películas, tales como:

- Películas con varios idiomas de reproducción.
- Películas creadas o filmadas en varios países.
- Películas con ganancias de cero.
- Películas sin puntuación de categoría.

(Se puede agregar más información aquí según el análisis realizado)

---

## Modelo para el Sistema de Recomendación

El modelo de recomendación está basado en la **similitud del coseno**, una medida matemática utilizada para medir la similitud entre dos vectores en un espacio de características. Esta técnica es especialmente útil en áreas como el procesamiento de texto, análisis de datos y aprendizaje automático, donde los vectores representan características de elementos, como palabras, documentos o productos.

Para la realización de este modelo, debido a las limitaciones de la plataforma Render para los servicios web, solo se podrán utilizar aproximadamente **5,000 registros** una vez que los datos hayan sido transformados.

---

## APIs

Las funciones solicitadas y sus **endpoints** son las siguientes:

1. **`cantidad_filmaciones_mes(Mes)`**:
   - **Descripción**: Se ingresa un mes en idioma español y devuelve la cantidad de películas estrenadas en ese mes.
   - **Ejemplo de retorno**: "X cantidad de películas fueron estrenadas en el mes de X."

2. **`cantidad_filmaciones_dia(Dia)`**:
   - **Descripción**: Se ingresa un día en idioma español y devuelve la cantidad de películas estrenadas en ese día.
   - **Ejemplo de retorno**: "X cantidad de películas fueron estrenadas en el día X."

3. **`score_titulo(titulo_de_la_filmacion)`**:
   - **Descripción**: Se ingresa el título de una película y devuelve el título, el año de estreno y el score.
   - **Ejemplo de retorno**: "La película X fue estrenada en el año X con un score/popularidad de X."

4. **`votos_titulo(titulo_de_la_filmacion)`**:
   - **Descripción**: Se ingresa el título de una película y devuelve el título, la cantidad de votos y el valor promedio de las votaciones. Si la película tiene menos de 2,000 valoraciones, se debe devolver un mensaje informando que no cumple con esta condición.
   - **Ejemplo de retorno**: "La película X fue estrenada en el año X. La misma cuenta con un total de X valoraciones, con un promedio de X."

5. **`get_actor(nombre_actor)`**:
   - **Descripción**: Se ingresa el nombre de un actor y se devuelve el éxito de este actor, medido a través de su retorno, además de la cantidad de películas en las que ha participado y el promedio de retorno.
   - **Ejemplo de retorno**: "El actor X ha participado en X cantidad de filmaciones, y ha conseguido un retorno de X con un promedio de X por filmación."

6. **`get_director(nombre_director)`**:
   - **Descripción**: Se ingresa el nombre de un director y se devuelve el éxito de este director, medido a través del retorno de sus películas. Además, se debe devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.

7. **`recomendacion(titulo)`**:
   - **Descripción**: Se ingresa el nombre de una película y se devuelven las 5 películas más similares, basadas en la similitud de coseno.
   
---

## Herramientas Tecnológicas

- **Python**.
- **FastAPI**.
- **Uvicorn**.
- **GitHub**.
- **Render**.