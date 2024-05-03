from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:1234@localhost:3306/colaboradores") #root seria el usuario y luego la contraseña de la db.
                                                                #el localhost:3306 es el puerto y dsp / iria la base de datos                                                            
meta = MetaData()

conn = engine.connect().execution_options(isolation_level="AUTOCOMMIT")

