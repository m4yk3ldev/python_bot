from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


# Model
class User(Base):
    __tablename__ = 'user'

    id = Column('id', Integer, primary_key=True)
    username = Column('username', String, unique=True)
    correo = Column('correo', String, unique=True)
    telefono = Column('telefono', String, unique=True, nullable=True)
    provincia = Column('prov', String)
    is_3d = Column('is_3d', Boolean)

    def setCorreo(self, email):
        self.correo = email

    def setTelefono(self, telef):
        self.telefono = telef

    def setProvincia(self, prov):
        self.provincia = prov

    def setUsername(self, us):
        self.username = us


# Crear conexion
engine = create_engine('sqlite:///db.sqlite', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()


def AddUser(user):
    try:
        session.add(user)
    except ValueError:
        pass


def Salvar():
    session.commit()


def CerrarConexion():
    session.close()
