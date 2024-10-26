from sqlalchemy import Column, Integer, String, Boolean, Date
from datetime import date, datetime
import db

class Tarea(db.Base):
    __tablename__ = "tarea"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True)
    contenido = Column(String(200), nullable=False)
    hecha = Column(Boolean)
    fecha_limite = Column(Date, default=date.today)
    categoria = Column(String, nullable=True)


    def __init__(self, contenido, hecha,categoria, fecha_limite=None):
        self.contenido = contenido
        self.hecha = hecha
        self.categoria=categoria
        self.fecha_limite = fecha_limite or date.today()


    def __str__(self):
        return "Tarea({}:,{}, {},{},{})".format(self.id, self.contenido,self.hecha,self.categoria,self.fecha_limite)
