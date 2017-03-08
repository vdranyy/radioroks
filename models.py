from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Date(Base):
    __tablename__ = "dates"
    id = Column(Integer, primary_key=True)
    date = Column(Date, unique=True)
    music_tracks = relationship("MusicTrack", backref="date",
                                lazy="dynamic")

    def __repr__(self):
        return "<Date {date}>".format(date=self.date)


class MusicTrack(Base):
    __tablename__ = "musictracks"
    id = Column(Integer, primary_key=True)
    artist = Column(String(256))
    song = Column(String(256))
    date_id = Column(Integer, ForeignKey("dates.id"))

    def __repr__(self):
        return "<MusicTrack ({artist}: {song})>".format(
            artist=self.artist,
            song=self.song
        )
