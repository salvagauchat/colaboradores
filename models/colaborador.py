from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

colaboradores = Table("colaborador", meta,
    Column('id', Integer, primary_key=True),
    Column('fullname', String(255)),
    Column('nombre', String(255),nullable=True),
    Column('apellido', String(255),nullable=True),
    Column('email', String(255),nullable=True),
    Column('userAD', String(255), nullable=True),
    )

canales = Table("canales", meta,
    Column('id', Integer, primary_key=True),
    Column('webex', String(255)),
    Column('whatsapp', String(255), nullable=True),
    Column('email', String(255), nullable=True),
    Column('proyecto', String(255)), #FORENKEY de la tabla proyecto de la db
    )

referentes = Table("referentes", meta,
    Column('id', Integer, primary_key=True),
    Column('proyecto', String(255)), #FORENKEY de la tabla proyecto de la db
    Column('lider_tecnico_id', Integer, ForeignKey('colaborador.id')),
    Column('lider_tribu_id', Integer, ForeignKey('colaborador.id')), 
    Column('po_id', Integer, ForeignKey('colaborador.id')),
)

meta.create_all(bind=engine, tables=[colaboradores, canales, referentes])