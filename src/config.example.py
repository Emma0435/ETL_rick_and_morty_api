#Renombrar este archivo como "config.py"
#Ejemplo de la conexión a la base de datos de PostgreSQL 
from sqlalchemy import create_engine

usuario = 'TU_USUARIO'
contraseña = 'TU_CONTRASEÑA'
host = 'localhost'
puerto = '5432'
nombre_bd = 'TU_BASE_DE_DATOS'

engine = create_engine(
    f'postgresql+psycopg2://{usuario}:{contraseña}@{host}:{puerto}/{nombre_bd}',
    connect_args={'client_encoding': 'utf8'}
)

try:
    with engine.connect() as conexion:
        print('Conexion exitosa')
except Exception as e:
    print(f'Error en la conexión: {e}')