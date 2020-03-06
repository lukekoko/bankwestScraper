from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import config

settings = config.settings
SQLALCHEMY_DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(settings['sql_type'], settings['sql_user'], settings['sql_pass'], settings['sql_host'], settings['sql_port'], settings['sql_database'])

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()