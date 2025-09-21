import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PyQt6.QtCore import QSettings

from app.db.models import BaseModel

def get_current_path():
    project_root = os.path.dirname(os.path.abspath(__file__))
    lib_path = os.path.join(project_root, "lib")

    os.makedirs(lib_path, exist_ok=True)

    return lib_path

config = QSettings('config.ini', QSettings.Format.IniFormat)
config.setValue('User/Folder', get_current_path())

def init_db(engine):
    BaseModel.metadata.create_all(bind=engine)

def get_current_session():
    DEFAULT_PATH = str(config.value('User/Folder', '/'))
    engine = create_engine(url=f'sqlite:///{DEFAULT_PATH}/app.db', echo=True)
    init_db(engine)
    session_maker = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return session_maker()