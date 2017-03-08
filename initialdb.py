from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Date, MusicTrack


engine = create_engine("sqlite:///radioroks.sqlite", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)
