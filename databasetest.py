import sqlite3
import itertools
import gi
from miner import miner
from reproductor import *
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class database(object):
    def __init__(self,dir,list,paths):
        self.dir = dir
        self.list = []
        self.paths = []
        self.list = list
        self.paths = paths

    def create_database(self):
        db = sqlite3.connect("Reproductor.sqlite")
        db.execute("create table types(id_type integer primary key,description text)")
        db.execute(
            "create table performers(id_performer integer primary key,name text ,id_type integer,foreign  key  (id_type) references types(id_type))")
        db.execute(
            "create table persons (id_person integer primary key,stage_name text, real_name text,birth_date text,death_date text)")
        db.execute("create table groups (id_group integer primary  key,name text,start_date text,end_date text)")
        db.execute("create table albums(id_album integer primary key,path text,name text,year integer)")
        db.execute(
            "create table rolas(id_rola integer primary key,id_performer integer ,id_album integer,path text,title text,track integer,year integer,genre text,foreign key (id_performer) references performer(id_performer),foreign  key (id_album) references albums(id_album))")
        db.execute(
            "create table in_group(id_person integer,id_group integer ,primary  key (id_person,id_group),foreign key (id_person) references persons(id_person),foreign key (id_group) references  groups(id_group))")
        db.execute("insert into types values(0,'Person')")
        db.execute("insert into types values(1,'Group')")
        db.execute("insert into types values(2,'Unknown')")
        db.commit()
        db.close()
    def fill_database(self):
        db = sqlite3.connect("Reproductor.sqlite")
        for file,path in zip(self.list,self.paths):
            if file.track.isdigit():
                trackS = file.track
            else:
                trackS = file.track.rsplit("/",1)[0]
            track = int(trackS)
            rolas_params = (file.artist,file.album,path,file.song,track,file.year,file.genre)
            performers_params = (2,file.artist,file.artist)
            reformed = path.rsplit("/", 1)[0]
            reformed += '/'
            album_params = (reformed, file.album, file.year,reformed,file.album)
            db.execute("insert into performers(id_type,name) select ?,? where not exists (select * from performers where name = ?)", performers_params)
            db.execute("insert into albums (path,name,year) select ?,?,? where not exists (select * from albums where path =  ? and name = ?)",album_params)
            db.execute("insert into rolas (id_performer,id_album,path,title,track,year,genre) select (select performers.id_performer from performers where performers.name = ?),(select albums.id_album from albums where albums.name = ?),?,?,?,?,?", rolas_params)
        db.commit()
        db.close()




minero = miner("ola")
minero.find_mp3_files()
lista = minero.get_mp3_tags()
paths = minero.mp3_files_path
data = database("hello",lista,paths)
data.create_database()
data.fill_database()


win = TreeViewFilterWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

