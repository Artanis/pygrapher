# -*- coding: UTF-8 -*-

import gtk
import math
from math import *
from time import time

import ui
import plotter
import renderer

def expose_graph (draw, event):
    x, y, w, h = draw.get_allocation()
    cr = draw.window.cairo_create()
    
    # create renderer
    canvas = renderer.Graph((w, h), ui.resolution())
    
    # Get graphs
    functions = []
    
    # kinda nice, this function definition anywhere ability.
    # This creates plotter.Function objects for each active function
    # in the TreeStore.
    def foreach_cb(treemodel, treepath, treeiter, selection):
        if treemodel[treepath][1] and treemodel[treepath][0] != "":
            highlight = selection.iter_is_selected(treeiter)
            functions.append(plotter.Function(treemodel[treepath][0], highlight))
    ui.store_plot.foreach(foreach_cb, ui.tree_plot.get_selection())
    
    del(foreach_cb) # Don't need it anymore.
    
    graph = canvas.render(functions, ui.trace())
    
    cr.set_source_surface(graph)
    cr.rectangle(0,0,w,h)
    cr.fill()

def refresh_graph(btn):
    expose_graph(ui.draw_graph, None)

ui.ui_tree.get_widget("btn_refresh").connect("clicked", refresh_graph)
ui.draw_graph.connect("expose-event", expose_graph)

ui.window_main.show_all()
gtk.main()
