import sqlite3

db = sqlite3.connect("Reproductor.sqlite")
db.execute("create table types(id_type integer primary key,description text)")
db.execute("create table performers(id_performer interger primary key, id_type integer,foreign  key  (id_type) references types(id_type))")
db.execute("create table persons (id_person integer primary key,stage_name text, real_name text,birth_date text,death_date text)")
db.execute("create table groups (id_group integer primary  key,name text,start_date text,end_date text)")
db.execute("create table albums(id_album integer primary key,path text,name text,year integer)")
db.execute("create table rolas(id_rola integer primary key,id_performer integer ,id_album integer,path text,title text,track integer,year integer,genre text,foreign key (id_performer) references performer(id_performer),foreign  key (id_album) references albums(id_album))")
db.execute("create table in_group(id_person integer,id_group integer ,primary  key (id_person,id_group),foreign key (id_person) references persons(id_person),foreign key (id_group) references  groups(id_group))")
db.execute("insert into types values(0,'Person')")
db.execute("insert into types values(1,'Group')")
db.execute("insert into types values(2,'Unknown')")
db.execute("insert into albums values(2,'Unknown','espora',1008)")

"""
cursor = db.cursor()
cursor.execute("select * from types")

for id_type,description in cursor:
   print(id_type)
   print(description)
   print("-"*20)

cursor.execute("select * from albums")

for id_album,path,text,year in cursor:
    print(text)
    print(year)
    print("-"*20)

cursor.close()
"""
db.close()
