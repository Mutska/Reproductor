import gi
import os
import sqlite3
import itertools

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

tup = ()
lista = []
db = sqlite3.connect("Reproductor.sqlite")
cursor = db.cursor()

cursor.execute("select * from rolas,performers,albums where rolas.id_performer = performers.id_performer and rolas.id_album = albums.id_album")

for record in cursor:
   tup = (record[4],record[9],record[13],record[7])
   lista.append(tup)
cursor.close()

db.close()
#print(lista)


def get_path(rel_path):
    dir_of_py_file = os.path.dirname(__file__)
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource


class DialogExample(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Edit Persons", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        hbox = Gtk.HBox()
        hbox2 = Gtk.HBox()
        hbox3 = Gtk.HBox()
        hbox4 = Gtk.HBox()
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
        box = self.get_content_area()
        box.set_spacing(5)
        box.add(hbox)
        box.add(hbox2)
        box.add(hbox3)
        box.add(hbox4)
        self.show_all()


class DialogExample2(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Edit Group", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        hbox = Gtk.HBox()
        hbox2 = Gtk.HBox()
        hbox3 = Gtk.HBox()
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
        box = self.get_content_area()
        box.set_spacing(5)
        box.add(hbox)
        box.add(hbox2)
        box.add(hbox3)
        self.show_all()


class DialogWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Editions")
        self .set_border_width(6)
        self.box = Gtk.Box(spacing=6)
        self.add(self.box)
        self.button1 = Gtk.Button(label="Edit Persons")
        self.button1.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.button1, True, True, 0)
        self.button2 = Gtk.Button(label="Edit Groups")
        self.button2.connect("clicked", self.on_button_clicked2)
        self.box.pack_start(self.button2, True, True, 0)

    def on_button_clicked(self, widget):
        dialog = DialogExample(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()

    def on_button_clicked2(self, widget):
        dialog = DialogExample2(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

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

        #Creacion del "ListStore model"
        self.fields = Gtk.ListStore(str, str, str,str)
        for titles in lista:
            self.fields.append(list(titles))
        self.current_filter_search = []

        #Creacion del  filter con el "liststore model"
        self.search_filter = self.fields.filter_new()
        #setting the filter function, note that we're not using the
        #self.search_filter.set_visible_func(self.search_filter_func)

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
                self.img1.set_from_icon_name("emblem-system", 1)
                button.set_image(self.img1)
            if i == 2:
                self.img1 = Gtk.Image()
                self.img1.set_from_icon_name("avatar-default", 1)
                button.set_image(self.img1)

            button.set_image_position(Gtk.PositionType.RIGHT)
            button.connect("clicked", self.on_entry_enter)

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
            print(model[iter][0])
            win = DialogWindow()
            #win.connect("destroy", Gtk.main_quit)
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
        # setting the filter function, note that we're not using the
        self.search_filter.set_visible_func(self.search_filter_func)
        # Actualizamos "filter" para que actualize la vista
        self.search_filter.refilter()

    def on_enter(self,widget):
        text = widget.get_text()
        print(text)
        return text



win = TreeViewFilterWindow()
#print(dir(win.props))
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
