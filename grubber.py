import re
import datetime
import time
import urllib.request as request
from initialdb import session
from models import Date, MusicTrack


def get_date():
    date_today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    date_yesterday = date_today - delta
    return date_yesterday


def get_date_for_url(date):
    year, month, day, *_ = date.timetuple()
    if month < 10:
        month = "0{0}".format(month)
    if day < 10:
        day = "0{0}".format(day)
    date = "{day}-{month}-{year}".format(
        day=day, month=month, year=year)
    return date


def get_url(date):
    url = "http://www.radioroks.ua/playlist/{date}.html".format(
        date=get_date_for_url(date))
    return url


def grub_data_from_url(date):
    response = request.urlopen(get_url(date))
    response = response.readlines()

    for i in response:
        line = i.decode("utf-8").rstrip("\n")
        line = line.lstrip()
        if line.startswith("<div  data-singer"):
            artist = re.search('(?<=<div  data-singer=")([^\"><]+)', line)
            song = re.search('(?<=data-song=")([^\"><]+)', line)
            yield ((artist.group(0), song.group(0)))


def save_data_to_db():
    date = session.query(Date).filter_by(date=get_date()).first()
    if date is None:
        grubber_date = get_date()
        date = Date(date=grubber_date)
        session.add(date)
        session.commit()
        music_data = grub_data_from_url(grubber_date)
        for item in music_data:
            music_track = MusicTrack()
            music_track.date_id = date.id
            music_track.artist = item[0]
            music_track.song = item[1]
            session.add(music_track)
            session.commit()
        print("Data has been loaded successfully")
    else:
        print("Date is already stored in the database")
    time.sleep(86400)


if __name__ == "__main__":
    while True:
        save_data_to_db()
