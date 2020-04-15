from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


# Model
class User(Base):
    __tablename__ = 'user'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String, unique=True)
    correo = Column('correo', String, unique=True)
    telefono = Column('telefono', String, unique=True, nullable=True)
    provincia = Column('prov', String)
    is_3d = Column('is_3d', Boolean, default=False)
    cant_fdm = Column('cant_fdm', Integer, nullable=True)
    diamtro_filamento = Column('diametro_filamento', String, nullable=True)
    cant_printerSLA_DLP = Column('cant_printerSLA_DLP', Integer, nullable=True)
    is_cnc = Column('is_cnc', Boolean, default=False)
    cant_cnc = Column('cant_cnc', Integer, nullable=True)
    materiales_cnc = Column('metariales_cnc', String, nullable=True)

    def setCorreo(self, email):
        self.correo = email

    def setTelefono(self, telef):
        self.telefono = telef

    def setProvincia(self, prov):
        self.provincia = prov

    def setUsername(self, us):
        self.username = us

    def setCantFDM(self, cant):
        self.cant_fdm = cant

    def setDiametroFilamento(self, diam):
        self.diamtro_filamento = diam

    def setCantSLA_DLP(self, csd):
        self.cant_printerSLA_DLP = csd

    def setIsCNC(self):
        self.is_cnc = True

    def setIs3D(self):
        self.is_3d = True

    def setCantCNC(self, cnc):
        self.cant_cnc = cnc

    def setMaterialesCNC(self, cnc):
        self.materiales_cnc = cnc


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
