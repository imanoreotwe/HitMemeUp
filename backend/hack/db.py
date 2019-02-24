from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('mysql+mysqldb://admin@imaoreo.io:3306/service?host=localhost?port=3306', convert_unicode=True)
engine = create_engine('mysql+mysqldb://root:jad3Bis0n@imaoreo.io:3306/service', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import hack.models
    Base.metadata.create_all(bind=engine)
