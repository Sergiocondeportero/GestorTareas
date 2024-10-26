from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cambiado "check_same:thread" a "check_same_thread"
engine = create_engine("sqlite:///database/tareas.db",
                       connect_args={"check_same_thread": False})  # Nombre correcto del argumento

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
