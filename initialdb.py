import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Date, MusicTrack


USER = os.environ.get("RADIOROKS_USER")
PASSWORD = os.environ.get("RADIOROKS_PASSWORD")
HOST = "localhost"
PORT = 5432
DB = "radioroks"


url = "postgresql://{user}:{password}@{host}:{port}/{db}"
url = url.format(user=USER,
                 password=PASSWORD,
                 host=HOST,
                 port=PORT,
                 db=DB)


engine = create_engine(url, client_encoding="utf8")
Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)
