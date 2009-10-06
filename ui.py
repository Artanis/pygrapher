import gtk
import gtk.glade

__all__ = ["ui_tree", "window_main", "store_plot", "tree_plot",
    "draw_graph", "status_main", "trace"]

def police_graphs(model, path, row_iter):
    row = model[path]
    if row.next is not None:
        if row[0] == "":
            model.remove(row_iter)
    elif row[0] != "":
        model.append(None, ["", False, None])

def onToggle(toggle, path, model):
	model[path][1] = not model[path][1]

def onEdited(cell, path, text, model):
	model[path][0] = text
	model[path][1] = True
	
	# Auto create/delete functions as needed
	model.foreach(police_graphs)

glade_ui = "ui.glade"
ui_tree = gtk.glade.XML(glade_ui)

signals = {
    "gtk_main_quit": gtk.main_quit,
}

ui_tree.signal_autoconnect(signals)

# function, draw, error
store_plot = gtk.TreeStore(str, bool, gtk.gdk.Pixbuf)
store_plot.append(None, ["((x**3 + 2*x**2 + 3*x + 4) / x) / 8", True, None])
store_plot.append(None, ["(x**2 + 2*x + 3) / 8", True, None])
store_plot.append(None, ["", False, None])

# Setup columns
# COLUMN str -- Function
col_function = gtk.TreeViewColumn("Function")

col_function_err_cell = gtk.CellRendererPixbuf()
col_function.pack_start(col_function_err_cell)

col_function_cell = gtk.CellRendererText()
col_function_cell.set_property("editable", True)
col_function_cell.connect("edited", onEdited, store_plot)
col_function.pack_start(col_function_cell)

col_function.add_attribute(col_function_cell, "text", 0)
col_function.add_attribute(col_function_err_cell, "pixbuf", 2)

# COLUMN bool -- Plot the function?
col_draw = gtk.TreeViewColumn()
col_draw_cell = gtk.CellRendererToggle()
col_draw_cell.set_property("activatable", True)
col_draw_cell.connect("toggled", onToggle, store_plot)
col_draw.pack_start(col_draw_cell)
col_draw.add_attribute(col_draw_cell, "active", 1)

tree_plot = ui_tree.get_widget("tree_plot")
tree_plot.set_model(store_plot)
tree_plot.append_column(col_draw)
tree_plot.append_column(col_function)

draw_graph = ui_tree.get_widget("draw_graph")
window_main = ui_tree.get_widget("window_main")
status_main = ui_tree.get_widget("status_main")

# Prepare graph resolution
xmin = ui_tree.get_widget("spinner_graphwindow_x_min")
xmax = ui_tree.get_widget("spinner_graphwindow_x_max")
ymin = ui_tree.get_widget("spinner_graphwindow_y_min")
ymax = ui_tree.get_widget("spinner_graphwindow_y_max")

def trace():
    x_value = ui_tree.get_widget("spin_trace").get_value()
    b_trace = ui_tree.get_widget("chk_trace").get_active()
    return (b_trace, x_value)

def resolution():
    return (xmin.get_value(), xmax.get_value(),
        ymin.get_value(), ymax.get_value())

# Set default windowing values
xmin.set_value(-5.0)
xmax.set_value(5.0)
ymin.set_value(-5.0)
ymax.set_value(5.0)
