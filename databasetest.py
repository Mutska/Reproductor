import sqlite3

db = sqlite3.connect("Reproductor.sqlite")
db.execute("create table types(id_type integer primary key,description text)")
db.execute("insert into types values(0,'Person')")
db.execute("insert into types values(1,'Group')")
db.execute("insert into types values(2,'Unknown')")

cursor = db.cursor()
cursor.execute("select * from types")

for id_type,description in cursor:
    print(id_type)
    print(description)
    print("-"*20)

cursor.close()
db.close()