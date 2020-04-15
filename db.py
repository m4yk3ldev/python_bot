from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    cant_printerSLA_DLP = Column('cant_printerSLA_DLP', Integer)
    is_cnc = Column('is_cnc', Boolean, default=False)
    cant_cnc = Column('cant_cnc', Integer)
    materiales_cnc = Column('metariales_cnc', String, nullable=True)
    cant_pla = Column('cant_pla', Integer)
    cant_petg = Column('cant_petg', Integer)
    cant_abs = Column('cant_abs', Integer)
    cant_tpu = Column('cant_tpu', Integer)
    cant_litro_resina = Column('cant_litro_resina', Integer)
    tipo_resina = Column('tipo_resina', String)
    m2_acrilico = Column('m2_acrilico', Integer)
    espesor_acrilico = Column('espesor_acrilico', String)
    m2_pvc = Column('m2_pvc', Integer)
    espesor_pvc = Column('espesor_pvc', String)
    m2_plied_madera = Column('m2_plied_madera', Integer)
    espesor_plied_madera = Column('espesor_plied_madera', String)

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

    def setCantPLA(self, pla):
        self.cant_pla = pla

    def setCantPETG(self, petg):
        self.cant_petg = petg

    def setCantABS(self, abs):
        self.cant_abs = abs

    def setCantTPU(self, tpu):
        self.cant_tpu = tpu

    def setCantLitroResina(self, resina):
        self.cant_litro_resina = resina

    def setTipoResina(self, resina):
        self.tipo_resina = resina

    def setM2Acrilico(self, m2):
        self.m2_acrilico = m2

    def setEspesorAcrilico(self, acrilico):
        self.espesor_acrilico = acrilico

    def setM2PVC(self, m2):
        self.m2_pvc = m2

    def setEspesorPVC(self, pvc):
        self.espesor_pvc = pvc

    def setM2Plied_Madera(self, m2):
        self.m2_plied_madera = m2

    def setEspesorMadera(self, madera):
        self.espesor_plied_madera = madera

    def setID(self, id):
        self.id = id


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


def get_update_query(table_name, where_vals, update_vals):
    query = table_name.update()
    for k, v in where_vals.iteritems():
        query = query.where(getattr(table_name.c, k) == v)
    return query.values(**update_vals)
