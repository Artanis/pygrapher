import gtk
import gtk.glade
import pyglet

glade_ui = "ui.glade"
ui_tree = gtk.glade.XML(glade_ui)
signals = {
    "gtk_main_quit": gtk.main_quit
}
ui_tree.signal_autoconnect(signals)

# function, draw, line color, line width, line type
store_plot = gtk.TreeStore(str, bool, gtk.gdk.Color, int, int)
store_plot.append(None, ["sin(x)", True, gtk.gdk.Color(), 1, 1])

# Setup columns
col_draw = gtk.TreeViewColumn("Plot")


col_function = gtk.TreeViewColumn("Function")


# TODO: line color
# TODO: line width
# TODO: line style

tree_plot = ui_tree.get_widget("tree_plot")
tree_plot.append_column(col_draw)
tree_plot.append_column(col_function)
tree_plot.set_model(store_plot)


window_main = ui_tree.get_widget("window_main")
window_main.show_all()
gtk.main()
