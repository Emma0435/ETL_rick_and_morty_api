# funciones para conectarse a la API y traer datos crudos
import requests
import time
import json

def extraer_datos_paginados(url, json_name):
    print(f"Comenzando petición HTTP para {json_name}")
    todos_los_datos = []
    
    while url is not None:
        respuesta = requests.get(url)
        # print(respuesta.status_code)
        # print(respuesta.text)
        cuerpo = respuesta.json()
        
        #region Extend
        # Un extend es como un append, la diferencia es que si hago un append, el json estará
        # en el índice 0, si hago un extend, cada diccionario del json se colocará en un índice distinto
        # endregion
        todos_los_datos.extend(cuerpo["results"])
        url = cuerpo["info"]["next"]
        time.sleep(0.1)
    
    with open(f"src/json/{json_name}.json", "w", encoding="utf-8") as archivo:
        json.dump(todos_los_datos, archivo, ensure_ascii=False, indent=4)
    
    print(f'Json {json_name} creado')
                
    return todos_los_datos

# if __name__ == "__main__":
#     url_personaje = "https://rickandmortyapi.com/api/character"
#     personajes = extraer_datos_paginados(url_personaje, "personajes")
#     print(f"Cantidad personajes: {len(personajes)}")
    
#     url_ubicaciones = "https://rickandmortyapi.com/api/location"
#     ubicaciones = extraer_datos_paginados(url_ubicaciones, "ubicaciones")
#     print(f"cantidad ubicaciones: {len(ubicaciones)}")
    
#     url_episodios = "https://rickandmortyapi.com/api/episode"
#     episodios = extraer_datos_paginados(url_episodios, "episodios")
#     print(f"cantidad episodios: {len(episodios)}")