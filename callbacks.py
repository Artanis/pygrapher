import gtk

__all__ = ["signals"]

# Tree View Row Callbacks
def on_col_draw_cell_toggled(toggle, path, model):
    """ Toggles the draw field of the row in the store_plot
    
    """
    model[path][1] = not model[path][1]

def police_graphs(model, path, row_iter):
    """ TreeStore Foreach callback
    
    Removes row with if function definition is empty, unless it is the
    last (as in tail) row.
    
    """
    
    row = model[path]
    if row.next is not None:
        if row[0] == "":
            model.remove(row_iter)
    elif row[0] != "":
        model.append(None, ["", False, None])

def on_col_function_cell_edited(cell, path, text, model):
    """ Store new text for the row in store_plot
    
    Also cleans up the rows, removing those with empty definitions
    
    """
    
    model[path][0] = text
    model[path][1] = True
    
    # Auto create/delete functions as needed
    model.foreach(police_graphs)

def on_tree_plot_key_press_event(widget, event):
    print widget.get_selection()
    print event.keyval

signals = {
    "gtk_main_quit": gtk.main_quit,
    "on_tree_plot_key_press_event": on_tree_plot_key_press_event
}
