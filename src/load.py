# funciones para conectarse y escribir en PostgreSQL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, ForeignKey
from datetime import datetime #este es de python, el de arriba es de SQL 
import pandas as pd

#Creamos una base de las tablas en SQL 
class Base(DeclarativeBase):
    pass

#region Clases Tablas
# Es el "molde" que se usa para insertar y consultar datos
# también es el mapeo completo entre tu clase Python y la tabla SQL 
# de ahí el nombre ORM (Object-Relational Mapping).
#endregion
class Ubicacion(Base):
    #Nombre real de la tabla en PostgreSQL
    __tablename__ = 'ubicaciones'
    
    #region Mapped vd mapped_column
    # - Mapped[int]: habla puramente el idioma de Python. No sabe nada de SQL, 
    # solo describe "esto es un entero" para tu editor y para quien lea el código.

    # - mapped_column(...): habla puramente el idioma de SQL/base de datos. 
    # No sabe nada de tipado de Python, solo describe "esto es una columna INTEGER, primary key" para PostgreSQL.
    #endregion
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    dimension: Mapped[str] = mapped_column(String)
    created: Mapped[datetime] = mapped_column(DateTime)
    
class Episodio(Base):
    __tablename__ = 'episodios'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    air_date: Mapped[datetime] = mapped_column(DateTime)
    episodio: Mapped[str] = mapped_column(String)
    created: Mapped[datetime] = mapped_column(DateTime)
    
class Personaje(Base):
    __tablename__ = 'personajes'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    species: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)
    created: Mapped[datetime] = mapped_column(DateTime)
    
    #declaramos las llaves foráneas. ubicaciones en su columna id
    origin_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('ubicaciones.id'), nullable=True)
    location_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('ubicaciones.id'), nullable=True)
    
class Relacion_Personaje_Episodio(Base):
    __tablename__ = 'relacion_personaje_episodio'
    
    #region PK compuesta
    # Aqui no existe una columna id que identifique a cada registro por si solo
    # es decir, no hay un id autoincrementable.
    # Aqui la primary key esta hecha de la combinación de 2 columnas existentes
    
    # Por ejemplo:
    # La fila (personaje_id=5, episodio_id=3) solo puede exitir una única vez 
    #endregion
    personaje_id: Mapped[int] = mapped_column(Integer, ForeignKey('personajes.id'), primary_key=True)
    episodio_id: Mapped[int] = mapped_column(Integer, ForeignKey('episodios.id'), primary_key=True)

 
#  Creación de las tablas con la conexión a la BD
from .config import engine
from sqlalchemy.orm import Session
from sqlalchemy import inspect

#region Definición de función
# Esta función es la encargada de crear las tablas en la BD
# Utiliza la base que usamos también para la creación de la ESTRUCTURA
# y le damos de parámetro nuestra variable con la que creamos la conexión a la BD

# Base es el molde por cada clase 
# metadata es todos los moldes juntos (todas nuestras clases de tablas definidas antes)
# endregion
def crear_tablas():
    inspector = inspect(engine)
    
    tablas_bd = set(inspector.get_table_names()) #son las tablas existentes en la bd
    tablas_definidas = set(Base.metadata.tables.keys()) #son las clases que creamos anteriormente
    tablas_faltantes = tablas_definidas - tablas_bd #comparación de las tablas existentes con las que queremos que existan
    
    if tablas_faltantes == set():
        print('Esquema de tablas completo')
    else:
        print(f'Creando las tablas {tablas_faltantes}')
        Base.metadata.create_all(engine)
  
def cargar_ubicaciones(df_ubicaciones):
    with Session(engine) as session:
        # region Validacion
        #Consultamos los id's existntes en la BD, usamos ayuda de la clase para realizar la 
        # busqueda en la tabla
        # Esto es para evitar insertar datos ya existentes y no truene el código
        # endregion
        
        ids_existentes = session.query(Ubicacion.id).all() 
        # region Compresión de listas
        # ids = []    
        # for tupla in ids_existentes:
        #     id = tupla[0]
        #     ids.append(id) 
        # endregion  
        
        # esta línea es exactamente lo mismo que lo de arriba
        ids = [tupla[0] for tupla in ids_existentes]  
        ids = set(ids)
                        
        # region Explicacion corchetes y ~
        # asi como accedemos como df_ubicaciones['id'] para obtener la columna id,
        # Estamos consultando los valores en negación
        
        # Es decir: df_ubicaciones en el campo donde no estan los ids proporcionados
        # endregion
        df_filtrado = df_ubicaciones[~df_ubicaciones['id'].isin(ids)]
        
        if df_filtrado.empty:
            print('No hay ubicaciones nuevas que agregar a la BD')
        else:
            for _, fila in df_filtrado.iterrows():
                ubicacion = Ubicacion(
                    id = fila['id'],
                    name = fila['name'],
                    type = fila['type'],
                    dimension = fila['dimension'],
                    created = fila['created']
                )
                session.add(ubicacion)
            session.commit()
            
def cargar_episodios(df_episodios):
    with Session(engine) as sesion:
        episodios_existentes = sesion.query(Episodio.id).all()
        
        ids = [tupla[0] for tupla in episodios_existentes]
        ids = set(ids)
        
        df_filtrado = df_episodios[~df_episodios['id'].isin(ids)]
        
        if df_filtrado.empty:
            print('No hay episodios nuevos que agregar')
        else:
            for _, fila in df_filtrado.iterrows():
                episodio = Episodio(
                    id = fila['id'],
                    name = fila['name'],
                    air_date = fila['air_date'],
                    episodio = fila['episode'],
                    created = fila['created']
                )
                sesion.add(episodio)
            sesion.commit()

def cargar_personajes(df_personajes):
    with Session(engine) as session:
        personajes_existentes = session.query(Personaje.id).all()
        ids = [tupla[0] for tupla in personajes_existentes]
        ids = set(ids)
        
        df_filtrado = df_personajes[~df_personajes['id'].isin(ids)]
        
        if df_filtrado.empty:
            print('No hay personajes nuevos que agregar')
        else:
            for _, fila in df_filtrado.iterrows():
                personaje = Personaje(
                    id = fila['id'],
                    name = fila['name'],
                    status = fila['status'],
                    species = fila['species'],
                    type = fila['type'],
                    gender = fila['gender'],
                    image = fila['image'],
                    created = fila['created'],
                    
                    # region Validación de Nulos
                    # Hacemos una validación para saber si el campo es nulo o no
                    # De lo contrario la inserción de un NaN en la BD falla, entonces lo convertimos a None
                    # endregion
                    origin_id = None if (pd.isna(fila['origin_id'])) else fila['origin_id'],
                    location_id = None if (pd.isna(fila['location_id'])) else fila['location_id']
                )
                session.add(personaje)
            session.commit()
            
def cargar_relaciones(df_relacion):
    with Session(engine) as session:
        relaciones_existentes = set(session.query(Relacion_Personaje_Episodio.personaje_id, Relacion_Personaje_Episodio.episodio_id).all())  
        
        # region Zip
        # en el df tenemos 2 columnas, character y episode id, pero para hacer la comparación, necesitamos todo junto
        # con zip hacemos una concatenación de los 2 valores en una variable, en este caso una dupla
        # y creamos una lista de tuplas creadas con las 2 columnas del df
        # endregion  
        relaciones_dataframe = list(zip(df_relacion['character_id'], df_relacion['episode_id']))  
        
        # region Series
        # Una Series es una sola columna con índice; un DataFrame es una colección de Series.
        # Creamos una Series con las tuplas, usando el mismo índice de df_relacion para poder filtrar con ella.
        # endregion
        no_existe_en_db = ~pd.Series(relaciones_dataframe, index=df_relacion.index).isin(relaciones_existentes)
        
        df_filtrado = df_relacion[no_existe_en_db]  
        
        if df_filtrado.empty:
            print('No hay una relación nueva que agregar') 
        else:
            for _, fila in df_filtrado.iterrows():
                relacion = Relacion_Personaje_Episodio(
                    personaje_id = int(fila['character_id']),
                    episodio_id = int(fila['episode_id'])
                )
                session.add(relacion)
            session.commit()       
                
# if __name__ == '__main__':
#     crear_tablas()
    
    # print('__________________________________________')
    
    # print("Cargando ubicaciones...")
    # ubicaciones = transform.crear_tabla_ubicaciones()
    # cargar_ubicaciones(ubicaciones)
    
    # print('__________________________________________')
    
    # print('Cargando episodios...')
    # episodios = transform.crear_tabla_episodios()
    # cargar_episodios(episodios)
    
    # print('__________________________________________')
    
    # print('Cargando personajes...')
    # personajes = transform.crear_tabla_personajes()
    # cargar_personajes(personajes)
    
    # print('Cargando relaciones...')
    # relaciones = transform.crear_relacion_personaje_episodio()
    # cargar_relaciones(relaciones)
    # print('Proceso terminado')
    