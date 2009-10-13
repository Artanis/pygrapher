import re
import gtk

import plotter

__all__ = []

def store_plot_to_list_cb(treemodel, treepath, treeiter, user_data):
    functions, selection = user_data
    if treemodel[treepath][0] != "":
        if selection is not None:
            highlight = selection.iter_is_selected(treeiter)
        else: highlight = False
        functions.append(
            plotter.Function(
                treemodel[treepath][0],
                treemodel[treepath][1],
                highlight))

def store_plot_police_cb(model, path, row_iter):
    row = model[path]
    if row.next is not None:
        if row[0] == "":
            model.remove(row_iter)
    elif row[0] != "":
        model.append(None, ["", False])
    else:
        model[path][1] = False

# Tree View Row Callbacks
def on_col_draw_cell_toggled(toggle, path, model):
    """ Toggles the draw field of the row in the store_plot
    
    """
    model[path][1] = not model[path][1]

def on_col_function_cell_edited(cell, path, text, model):
    """ Store new text for the row in store_plot
    
    Also cleans up the rows, removing those with empty definitions
    
    """
    
    model[path][0] = text
    model[path][1] = True
    
    model.foreach(store_plot_police_cb)

def on_tree_plot_key_press_event(widget, event):
    pass
    #print widget.get_selection()
    #print event.keyval

def on_graphwindow_changed(widget, value, graph):
    graph.queue_draw()

"""
def on_draw_graph_drag_begin(widget, context, prev):
    icon = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, 1, 1)
    context.set_icon_pixbuf(icon, 10, 10)
    prev[0] = (0,0)
    print "Drag START"

def on_draw_graph_drag_motion(widget, context, x, y, time, res_controls, graph, prev):
    c_x, c_y, c_w, c_h = graph.get_allocation()
    
    spin_xmin = res_controls[0]
    spin_xmax = res_controls[1]
    spin_ymin = res_controls[2]
    spin_ymax = res_controls[3]
    
    xmin = spin_xmin.get_value()
    xmax = spin_xmax.get_value()
    ymin = spin_ymin.get_value()
    ymax = spin_ymax.get_value()
    
    canvas_x = lambda x: (x - xmin) * c_w / (xmax - xmin)
    canvas_y = lambda y: (ymax - y) * c_h / (ymax - ymin)
    canvas_point = lambda x,y: (canvas_x(x), canvas_y(y))
    graph_x = lambda x: x * (xmax - xmin) / c_w + xmin
    graph_y = lambda y: ymax - (y * (ymax - ymin) / c_h)
    graph_point = lambda x,y: (graph_x(x), graph_y(y))
    
    p_x, p_y = prev[0]
    prev[0] = (x, y)
    
    v_x, v_y = x - p_x, y - p_y
    
    print "Dragging", (v_x, v_y), time
"""

def on_draw_graph_drag_end(widget, context, prev):
    print "Drag END", prev[0]

def on_draw_graph_scroll_event(widget, event, res_controls, graph):
    direction = 1.0
    
    if event.direction is gtk.gdk.SCROLL_UP:
        # Zoom IN
        direction = 0.5
    elif event.direction is gtk.gdk.SCROLL_DOWN:
        # Zoom OUT
        direction = 2.0
    
    for spinner in res_controls:
        value = spinner.get_value()
        spinner.set_value(value * direction)
    
    graph.queue_draw()
    
    return True

def on_menu_main_graph_new_activate(widget, treestore):
    treestore.clear()
    treestore.append(None, ["", False])

def on_menu_main_graph_save_activate(widget, treestore):
    chooser = gtk.FileChooserDialog(title=None,
        action=gtk.FILE_CHOOSER_ACTION_SAVE,
        buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_SAVE_AS, gtk.RESPONSE_OK))
    filefilter = gtk.FileFilter()
    filefilter.set_name("Function List")
    filefilter.add_pattern("*.fn")
    chooser.add_filter(filefilter)
    
    response = chooser.run()
    if response == gtk.RESPONSE_OK:
        functions = []
        treestore.foreach(store_plot_to_list_cb, (functions, None))
        save_file = open(chooser.get_filename(), "w")
        for function in functions:
            save_file.write(str(function)+"\n")
    chooser.destroy()

def on_menu_main_graph_open_activate(widget, treestore):
    chooser = gtk.FileChooserDialog(title=None,
        action=gtk.FILE_CHOOSER_ACTION_SAVE,
        buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    filefilter = gtk.FileFilter()
    filefilter.set_name("Function List")
    filefilter.add_pattern("*.fn")
    chooser.add_filter(filefilter)
    
    response = chooser.run()
    if response == gtk.RESPONSE_OK:
        open_file = open(chooser.get_filename(), "r")
        parse = re.compile("f\(x\)\s=\s(.*)", re.I).match
        
        treestore.clear()
        
        for line in open_file:
            fn = parse(line)
            if fn is not None:
                treestore.append(None, [fn.group(1), True])
            #treestore.append(
    chooser.destroy()
    treestore.foreach(store_plot_police_cb)

