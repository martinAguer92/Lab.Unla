from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///gestor.db', echo=True) 


# Crear una sesión para interactuar con la base 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Declarar la base 
Base = declarative_base()


#Funcion para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()