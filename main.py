# orquesta todo: llama extract → transform → load en orden
from src import extract as E
# from src import transform as T
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