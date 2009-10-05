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
# COLUMN str -- Function
col_function = gtk.TreeViewColumn("Function")
col_function_cell = gtk.CellRendererText()
col_function.pack_start(col_function_cell)
col_function.add_attribute(col_function_cell, "text", 0)

# COLUMN bool -- Plot the function?
col_draw = gtk.TreeViewColumn("Plot")
col_draw_cell = gtk.CellRendererToggle()
col_draw.pack_start(col_draw_cell)
col_draw.add_attribute(col_draw_cell, "activatable", 1)

# COLUMN gtk.gdk.Color -- Line color
# TODO: line color

# COLUMN int -- Line width
# TODO: line width

# COLUMN int -- Line style
# TODO: line style

tree_plot = ui_tree.get_widget("tree_plot")
tree_plot.set_model(store_plot)
tree_plot.append_column(col_draw)
tree_plot.append_column(col_function)


window_main = ui_tree.get_widget("window_main")
window_main.show_all()
gtk.main()
