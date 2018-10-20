import gi
import os
import sqlite3
import itertools

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def get_path(rel_path):
    dir_of_py_file = os.path.dirname(__file__)
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource


class Edit_persons(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Edit Persons", parent, 0)
        hbox = Gtk.HBox()
        hbox2 = Gtk.HBox()
        hbox3 = Gtk.HBox()
        hbox4 = Gtk.HBox()
        hbox5 = Gtk.HBox()

        button = Gtk.Button()
        button.set_label("Save")
        button2 = Gtk.Button()
        button2.set_label("Cancel")

        self.set_default_size(300, 200)
        entry = Gtk.Entry()
        entry2 = Gtk.Entry()
        entry3 = Gtk.Entry()
        entry4 = Gtk.Entry()
        label = Gtk.Label("Stage name: ")
        label2 = Gtk.Label("Real name:   ")
        label3 = Gtk.Label("Date of birth: ")
        label4 = Gtk.Label("Date of death:   ")
        hbox.pack_start(label, False, 2, 0)
        hbox.pack_end(entry, True, True, 0)
        hbox2.pack_start(label2, False, 2, 0)
        hbox2.pack_end(entry2, True, True, 0)
        hbox3.pack_start(label3, False, 2, 0)
        hbox3.pack_end(entry3, True, True, 0)
        hbox4.pack_start(label4, False, 2, 0)
        hbox4.pack_end(entry4, True, True, 0)
        hbox5.pack_start(button, False, 2, 0)
        hbox5.pack_end(button2, True, True, 0)
        box = self.get_content_area()
        box.set_spacing(5)
        box.add(hbox)
        box.add(hbox2)
        box.add(hbox3)
        box.add(hbox4)
        box.add(hbox5)
        button.connect("clicked", self.saving, entry, entry2, entry3,entry4)
        self.show_all()

    def saving(self, widget, entry, entry2, entry3,entry4       ):
        stage_name = entry.get_text()
        real_name  = entry2.get_text()
        date_b = entry3.get_text()
        date_d = entry4.get_text()
        tup = (stage_name, real_name, date_b,date_d)
        db = sqlite3.connect("Reproductor.sqlite")
        cursor = db.cursor()
        cursor.execute("insert into persons(stage_name,real_name,birth_date,death_date) values(?,?,?,?)", tup)
        db.commit()
        cursor.close()
        db.close()


class Edit_groups(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Edit Group", parent, 0)

        hbox = Gtk.HBox()
        hbox2 = Gtk.HBox()
        hbox3 = Gtk.HBox()
        hbox4 = Gtk.HBox()

        button = Gtk.Button()
        button.set_label("Save")
        button2 = Gtk.Button()
        button2.set_label("Cancel")

        self.set_default_size(300, 200)
        entry = Gtk.Entry()
        entry2 = Gtk.Entry()
        entry3 = Gtk.Entry()
        label = Gtk.Label("Name: ")
        label2 = Gtk.Label("Start date:   ")
        label3 = Gtk.Label("End date: ")
        hbox.pack_start(label, False, 2, 0)
        hbox.pack_end(entry, True, True, 0)
        hbox2.pack_start(label2, False, 2, 0)
        hbox2.pack_end(entry2, True, True, 0)
        hbox3.pack_start(label3, False, 2, 0)
        hbox3.pack_end(entry3, True, True, 0)
        hbox4.pack_start(button, False, 2, 0)
        hbox4.pack_end(button2, True, True, 0)
        box = self.get_content_area()
        box.set_spacing(5)
        box.add(hbox)
        box.add(hbox2)
        box.add(hbox3)
        box.add(hbox4)
        button.connect("clicked", self.saving,entry, entry2, entry3)
        self.show_all()
    def saving(self,widget,entry,entry2,entry3):
        name = entry.get_text()
        start_date = entry2.get_text()
        end_date = entry3.get_text()
        tup = (name,start_date,end_date)
        db = sqlite3.connect("Reproductor.sqlite")
        cursor = db.cursor()
        cursor.execute("insert into groups(name,start_date,end_date) values(?,?,?)",tup)
        db.commit()
        cursor.close()
        db.close()


class Edit_on_groups_and_persons(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Editions")
        self .set_border_width(6)
        self.box = Gtk.Box(spacing=6)
        self.add(self.box)
        self.button1 = Gtk.Button(label="Edit Persons")
        self.button1.connect("clicked", self.on_button_persons)
        self.box.pack_start(self.button1, True, True, 0)
        self.button2 = Gtk.Button(label="Edit Groups")
        self.button2.connect("clicked", self.on_button_groups)
        self.box.pack_start(self.button2, True, True, 0)

    def on_button_persons(self, widget):
        dialog = Edit_persons(self)
        response = dialog.run()
        dialog.destroy()

    def on_button_groups(self, widget):
        dialog = Edit_groups(self)
        response = dialog.run()
        dialog.destroy()

class Edit_song(Gtk.Dialog):

    def __init__(self, parent,title,performer,album,genre):
        Gtk.Dialog.__init__(self, "Edit Song", parent, 0)

        button = Gtk.Button()
        button.set_label("Save")
        button2 = Gtk.Button()
        button2.set_label("Cancel")

        found = []
        db = sqlite3.connect("Reproductor.sqlite")
        cursor = db.cursor()
        cursor.execute("select rolas.track from rolas where title == ?",(title,)
            )
        for record in cursor:
            found.append(record[0])

        cursor.execute("select rolas.year from rolas where title == ?", (title,)
                       )
        for record in cursor:
            found.append(record[0])
        cursor.close()
        db.close()
        hbox = Gtk.HBox()
        hbox2 = Gtk.HBox()
        hbox3 = Gtk.HBox()
        hbox4 = Gtk.HBox()
        hbox5 = Gtk.HBox()
        self.set_default_size(300, 200)
        entry = Gtk.Entry()
        entry.set_text(title)
        entry2 = Gtk.Entry()
        entry2.set_text(str(found[0]))
        entry3 = Gtk.Entry()
        entry3.set_text(str(found[1]))
        entry4 = Gtk.Entry()
        entry4.set_text(genre)
        label = Gtk.Label("Title    : ")
        label2 = Gtk.Label("Track:   ")
        label3 = Gtk.Label("Year: ")
        label4 = Gtk.Label("Genre: ")
        hbox.pack_start(label, False, 2, 0)
        hbox.pack_end(entry, True, True, 0)
        hbox2.pack_start(label2, False, 2, 0)
        hbox2.pack_end(entry2, True, True, 0)
        hbox3.pack_start(label3, False, 2, 0)
        hbox3.pack_end(entry3, True, True, 0)
        hbox4.pack_start(label4, False, 2, 0)
        hbox4.pack_end(entry4, True, True, 0)
        hbox5.pack_start(button, True, True, 0)
        hbox5.pack_end(button2, True, True, 0)
        box = self.get_content_area()
        box.set_spacing(5)
        box.add(hbox)
        box.add(hbox2)
        box.add(hbox3)
        box.add(hbox4)
        box.add(hbox5)
        button.connect("clicked", self.saving,title,entry,entry2,entry3,entry4)
        self.show_all()
    def saving(self,widget,original_title,entry,entry2,entry3,entry4):
        title = entry.get_text()
        track = entry2.get_text()
        year = entry3.get_text()
        genre = entry4.get_text()
        tup = (title,track,year,genre,original_title)
        db = sqlite3.connect("Reproductor.sqlite")
        cursor = db.cursor()
        cursor.execute("update rolas set title = ?,track = ?,year = ?,genre = ? where rolas.title == ?",tup)
        db.commit()
        cursor.close()
        db.close()

class Edit_album(Gtk.Dialog):

    def __init__(self, parent,album):
        Gtk.Dialog.__init__(self, "Edit album", parent, 0)

        hbox = Gtk.HBox()
        hbox2 = Gtk.HBox()
        hbox3 = Gtk.HBox()
        self.set_default_size(300, 200)
        button = Gtk.Button()
        button.set_label("Save")
        button2 = Gtk.Button()
        button2.set_label("Cancel")
        found = []
        db = sqlite3.connect("Reproductor.sqlite")
        cursor = db.cursor()
        cursor.execute("select albums.name from albums where name == ?", (album,)
                       )
        for record in cursor:
            found.append(record[0])

        cursor.execute("select albums.year from albums where name == ?", (album,)
                       )
        for record in cursor:
            found.append(record[0])
        cursor.close()
        db.close()

        entry = Gtk.Entry()
        entry.set_text(album)
        entry2 = Gtk.Entry()
        entry2.set_text(str(found[1]))
        label = Gtk.Label("Name: ")
        label2 = Gtk.Label("Year:   ")
        hbox.pack_start(label, False, 2, 0)
        hbox.pack_end(entry, True, True, 0)
        hbox2.pack_start(label2, False, 2, 0)
        hbox2.pack_end(entry2, True, True, 0)
        hbox3.pack_start(button, False, 2, 0)
        hbox3.pack_end(button2, True, True, 0)
        box = self.get_content_area()
        box.set_spacing(5)
        box.add(hbox)
        box.add(hbox2)
        box.add(hbox3)
        button.connect("clicked", self.saving, album, entry, entry2)
        self.show_all()
    def saving(self, widget, original_title, entry, entry2):
        name = entry.get_text()
        year = entry2.get_text()
        tup = (name,  year, original_title)
        db = sqlite3.connect("Reproductor.sqlite")
        cursor = db.cursor()
        cursor.execute("update albums set name = ?,year = ? where albums.name == ?", tup)
        db.commit()
        cursor.close()
        db.close()
class Edit_performer(Gtk.Dialog):

    def __init__(self, parent,performer):
        Gtk.Dialog.__init__(self, "Edit performer", parent, 0)

        hbox = Gtk.HBox()
        hbox2 = Gtk.HBox()
        hbox3 = Gtk.HBox()

        self.set_default_size(300, 200)
        button = Gtk.Button()
        button.set_label("Save")
        button2 = Gtk.Button()
        button2.set_label("Cancel")
        found = []
        db = sqlite3.connect("Reproductor.sqlite")
        cursor = db.cursor()
        cursor.execute("select performers.name from performers where name == ?", (performer,)
                       )
        for record in cursor:
            found.append(record[0])

        cursor.execute("select performers.id_type from performers where name == ?", (performer,)
                       )
        for record in cursor:
            found.append(record[0])
        cursor.close()
        db.close()

        entry = Gtk.Entry()
        entry.set_text(performer)
        entry2 = Gtk.Entry()
        entry2.set_text(str(found[1]))
        label = Gtk.Label("Name: ")
        label2 = Gtk.Label("Type(0/1/2):   ")
        hbox.pack_start(label, False, 2, 0)
        hbox.pack_end(entry, True, True, 0)
        hbox2.pack_start(label2, False, 2, 0)
        hbox2.pack_end(entry2, True, True, 0)
        hbox3.pack_start(button, False, 2, 0)
        hbox3.pack_end(button2, True, True, 0)
        box = self.get_content_area()
        box.set_spacing(5)
        box.add(hbox)
        box.add(hbox2)
        box.add(hbox3)
        button.connect("clicked", self.saving, performer, entry, entry2)
        self.show_all()

    def saving(self, widget, performer, entry, entry2):
        name = entry.get_text()
        type = entry2.get_text()
        tup = (name, type, performer)
        db = sqlite3.connect("Reproductor.sqlite")
        cursor = db.cursor()
        cursor.execute("update performers set name = ?,id_type = ? where performers.name == ?", tup)
        db.commit()
        cursor.close()
        db.close()

class Songs(Gtk.Window):

    def __init__(self,title,performer,album,genre):
        Gtk.Window.__init__(self, title="Edit song properties")
        self .set_border_width(6)
        self.box = Gtk.Box(spacing=6)
        self.add(self.box)
        self.button1 = Gtk.Button(label="Edit Song")
        self.button1.connect("clicked", self.on_button_song,title,performer,album,genre)
        self.box.pack_start(self.button1, True, True, 0)
        self.button2 = Gtk.Button(label="Edit Album")
        self.button2.connect("clicked", self.on_button_album,album)
        self.box.pack_start(self.button2, True, True, 0)
        self.button3 = Gtk.Button(label="Edit Performer")
        self.button3.connect("clicked", self.on_button_performer,performer)
        self.box.pack_start(self.button3, True, True, 0)

    def on_button_song(self, widget,title,performer,album,genre):
        dialog = Edit_song(self,title,performer,album,genre)
        response = dialog.run()
        dialog.destroy()

    def on_button_album(self, widget,album):
        dialog = Edit_album(self,album)
        response = dialog.run()
        dialog.destroy()
    def on_button_performer(self, widget,performer):
        dialog = Edit_performer(self,performer)
        response = dialog.run()
        dialog.destroy()


class TreeViewFilterWindow(Gtk.Window):
    # Configuracion del window
    def __init__(self):
        Gtk.Window.__init__(self, title="Player")
        self.set_border_width(10)
        self.set_icon_from_file(get_path("index.png"))
        self.set_resizable(True)
        #Configuracion del grid
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)
        self.settings = Gtk.Settings.get_default()
        self.settings.props.gtk_button_images = True

        tup = ()
        lista = []
        db = sqlite3.connect("Reproductor.sqlite")
        cursor = db.cursor()

        cursor.execute(
            "select * from rolas,performers,albums where rolas.id_performer = performers.id_performer and rolas.id_album = albums.id_album")

        for record in cursor:
            tup = (record[4], record[9], record[13], record[7])
            lista.append(tup)
        cursor.close()
        db.close()

        #Creacion del "ListStore model"
        self.fields = Gtk.ListStore(str, str, str,str)
        for titles in lista:
            self.fields.append(list(titles))
        self.current_filter_search = []

        #Creacion del  filter con el "liststore model"
        self.search_filter = self.fields.filter_new()
        self.search_filter2 = self.fields.filter_new()


        #Creacion del  treeview, usando el  filter como  model.
        self.treeview = Gtk.TreeView.new_with_model(self.search_filter)
        self.treeview.connect("row-activated",self.on_db_click)
        for i, column_title in enumerate(["Title", "Artist", "Album","Genre"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)



        #Creacion de los button con sus respectivos eventos
        self.buttons = list()
        for i in range(3):
            button = Gtk.Button(label=None)
            self.buttons.append(button)
            if i == 0:
                self.img1 = Gtk.Image()
                self.img1.set_from_icon_name("media-playback-start", 1)
                button.set_image(self.img1)
                #button.connect("clicked",self._btn_cb)
            if i == 1:
                self.img1 = Gtk.Image()
                self.img1.set_from_icon_name("document-revert", 1)
                button.set_image(self.img1)
                button.connect("clicked",self.on_click_reformed)
            if i == 2:
                self.img1 = Gtk.Image()
                self.img1.set_from_icon_name("avatar-default", 1)
                button.set_image(self.img1)
                button.connect("clicked", self.on_enter)

            button.set_image_position(Gtk.PositionType.RIGHT)

        #Configuracion de un entry
        self.entry = Gtk.Entry()
        self.entry.connect("activate",self.on_entry_enter)
        self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,'system-search-symbolic')



        #Configuracion de la vista, (treeview in a scrollwindow)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.entry, self.buttons[2], Gtk.PositionType.RIGHT, 1, 1)
        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def on_db_click(self, tree_view,path,column):
            model = tree_view.get_model()
            iter = model.get_iter(path)
            title = model[iter][0]
            performer = model[iter][1]
            album = model[iter][2]
            genre = model[iter][3]
            win = Songs(title,performer,album,genre)
            win.show_all()

    def on_row_click(self,widget):
        print("Clickeando por diversion")

    def search_filter_func(self, model, iter, data):
        bools = []
        if self.current_filter_search is None or self.current_filter_search == "None":
            return True
        else:
            for  i  in range(len(self.current_filter_search)):
                bools.append(model[iter][0] == self.current_filter_search[i])
            tempo = False
            for i in range(len(bools)):
                tempo |= bools[i]
            return tempo
    def search_filter_func2(self, model, iter, data):
        return model[iter][0] != "PALABRASRESBUCADASAS"

    def on_entry_enter(self, widget):
        self.current_filter_search = []
        temp = widget.get_text()
        param = "%"
        param += temp
        param += "%"
        param_search = ( param, param,param )
        found = []
        db = sqlite3.connect("Reproductor.sqlite")
        cursor = db.cursor()
        cursor.execute(
            "select rolas.title,performers.name,albums.name from rolas,performers,albums where (rolas.id_performer = performers.id_performer and rolas.id_album = albums.id_album and (rolas.title like ? or performers.name like ? or albums.name like ?))",
            param_search)
        for record in cursor:
            found.append(record[0])
        self.current_filter_search = found
        cursor.close()
        db.close()
        print("Busqueda de patrón : %s" % temp)
        # Configuramos la funcion de filtrado
        self.search_filter.set_visible_func(self.search_filter_func)
        # Actualizamos "filter" para que actualize la vista
        self.search_filter.refilter()
    def on_click_reformed(self,widget):
        self.search_filter2.set_visible_func(self.search_filter_func2)
        self.search_filter2.refilter()

    def on_enter(self,widget):
        win = Edit_on_groups_and_persons()
        win.show_all()
