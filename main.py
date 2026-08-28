# orquesta todo: llama extract → transform → load en orden
from src import extract as E
from src import transform as T
# from src import load as L

if __name__ == "__main__":
    print('Comenzando etapa de Extracción...')
    
    url_personaje = "https://rickandmortyapi.com/api/character"
    personajes = E.extraer_datos_paginados(url_personaje, "personajes")
    
    url_ubicaciones = "https://rickandmortyapi.com/api/location"
    ubicaciones = E.extraer_datos_paginados(url_ubicaciones, "ubicaciones")
    
    url_episodios = "https://rickandmortyapi.com/api/episode"
    episodios = E.extraer_datos_paginados(url_episodios, "episodios")
    
    print('Etapa de extracción completada')
    print(60*'=')
    
    print('Comenzando etapa de Transformación...')
    personajes = T.crear_tabla_personajes()
    ubicaciones = T.crear_tabla_ubicaciones()
    episodios = T.crear_tabla_episodios()
    relacion_per_ep = T.crear_relacion_personaje_episodio()
    T.validacion_integridad(personajes, ubicaciones, episodios, relacion_per_ep)
    
    print('Etapa de transformación completada')
    print(60*'=')