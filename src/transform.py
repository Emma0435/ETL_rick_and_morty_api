# funciones de limpieza y transformación
import pandas as pd

'''
1 - convertir el json en tablas
2 - la columna origen guarda diccionarios, tipo de dato no viable en bases de datos 
3 - Guardar unicamente el ID del origen y la ubicación
'''
def crear_tabla_personajes():
    data = pd.read_json("src/json/personajes.json")

    df = pd.DataFrame(data)

    #region Explicación línea
    # creamos nueva columna "origen_url", leyendo el valor "url" de la columna "origin"
    # esto para separarlo del diccionario que es "origin"
    #endregion
    df["origin_url"] = df["origin"].apply(lambda x: x['url'])

    # region Separador de campos
    # creamos columna origen_id, en lugar de rescatar toda la URL para el personaje, solo salvamos el ID de su origen
    #la función lee la url, crea una lista de str, cada texto separado por un "/" es un campo, "[-1]" significa el último indice de la lista (es decir, el id)
    # endregion
    df['origin_id'] = df['origin_url'].apply(lambda x: x.split("/")[-1])
    
    # region Conversion de dato
    # origin_id guarda una string, con esta línea convertimos a entero
    # Pero en el json hay campos donde estan nulos, al querer convertir a entero truena
    #errors='coerce' convierte esa excepción a un null en la bd para que no truene
    # endregion
    df['origin_id'] = pd.to_numeric(df['origin_id'], errors='coerce')
    
    #repetimos los pasos para la ubicación 
    df['location_url'] = df["location"].apply(lambda x: x["url"])
    df['location_id'] = df['location_url'].apply(lambda x: x.split("/")[-1])
    df['location_id'] = pd.to_numeric(df['location_id'], errors='coerce')
    
    #region Eliminación de columas
    #eliminamos columnas que ya no son necesarias 
    #column_url y location_url solo fueron auxiliares para obtener el id
    # endregion
    df = df.drop(columns=['location', 'origin', 'url', 'location_url', 'origin_url'])
    
    return df

def crear_tabla_ubicaciones():
    data = pd.read_json("src/json/ubicaciones.json")
    
    df = pd.DataFrame(data)
    
    # region
    #eliminamos columna y le decimos que se "actualice"
    #asi evitamos hacer df = df.drop(...)
    # obtenemos el mismo resultado, solo es otra sintaxis
    #endregion
    df.drop(columns=['residents', 'url'], inplace=True)
        
    return df

def crear_relacion_personaje_episodio():
    data = pd.read_json('src/json/personajes.json')
    
    # region Fragmentar Json
    # creamos un dataframe reducido a unicamente 2 columnas
    # endregion
    df = pd.DataFrame(data[['id', 'episode']])
    
    df = df.rename(columns={'id': 'character_id'})
    
    # region Explode
        # un explode literalmente explota una estructura de datos
        # lo que hace es, en lugar de 1 id estar ligado a una lista de url's
        # ahora hace una tabla de muchos registros de url's ligadas a un id
        
        # EJEMPLO
        # Antes
            #     character_id   name    episode
            # 0             1   Rick    [1, 2, 3]
            # 1             2   Morty   [1, 5]
            
        # Después del explode
            #  character_id   name  episode
            #             1   Rick        1
            #             1   Rick        2
            #             1   Rick        3
            #             2  Morty        1
            #             2  Morty        5
            
        # por último indicamos que la columna a explotar es "episode"
        # endregion
    df = df.explode('episode')
    
    print(df[df['episode'].isnull()])
    
    df['episode_id'] = df['episode'].apply(lambda x: x.split('/')[-1])
    
    df['episode_id'] = pd.to_numeric(df['episode_id'], errors='coerce')
    
    df.drop(columns='episode', inplace=True)
        
    return df
    

if __name__ == "__main__":
    # crear_tabla_personajes()
    # crear_tabla_ubicaciones()
    crear_relacion_personaje_episodio()