import threading
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject, GLib
from get_data_from_api import get_data_from_api
from get_data_from_csv import get_data_from_csv


class MainWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="PAYCON")
        geometry = Gdk.Geometry()
        geometry.max_width = 800
        geometry.max_height = 600
        hints = Gdk.WindowHints(Gdk.WindowHints.MAX_SIZE)
        self.set_geometry_hints(None, geometry, hints)
        self.set_border_width(10)
        self.download_list = []
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        self.add(grid)

        self.software_liststore = Gtk.ListStore(str)
        for software_ref in self.download_list:
            i = [software_ref]
            self.software_liststore.append(i)

        self.treeview = Gtk.TreeView(model=self.software_liststore)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Заголовок", Gtk.CellRendererText(), text=0)
        self.treeview.append_column(column)

        button_api = Gtk.Button.new_with_label("Загрузить из API")
        button_api.connect("clicked", self.button_clicked, get_data_from_api)
        grid.add(button_api)

        button_file = Gtk.Button.new_with_label("Загрузить из файла")
        button_file.connect("clicked", self.button_clicked, get_data_from_csv)
        grid.attach(button_file, 1, 0, 1, 1)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        grid.attach_next_to(self.scrollable_treelist, button_api, Gtk.PositionType.BOTTOM, 2, 2)
        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def append_data_in_software_list(self, data):
        self.download_list = data
        for product in self.download_list:
            i = [product]
            self.software_liststore.append(i)

    def button_clicked(self, widget, func):
        dialog = DialogSpinner(self)
        dialog.show_all()

        def thread_run():
            self.append_data_in_software_list(func())
            GLib.idle_add(cleanup)

        def cleanup():
            dialog.destroy()
            t.join()

        t = threading.Thread(target=thread_run, args=[])
        t.start()


class DialogSpinner(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Загрузка", transient_for=parent, flags=0)

        self.set_default_size(150, 20)
        self.spinner = Gtk.Spinner()
        self.spinner.start()
        box = self.get_content_area()
        box.add(self.spinner)
        self.show_all()


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
