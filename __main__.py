# -*- coding: UTF-8 -*-

import gtk
import math
from math import *
from time import time

import ui
import plotter
import renderer
import callbacks

def expose_graph (draw, event):
    x, y, w, h = draw.get_allocation()
    cr = draw.window.cairo_create()
    
    # create renderer
    canvas = renderer.Graph((w, h), ui.resolution())
    
    # Get graphs
    functions = []

    ui.store_plot.foreach(callbacks.store_plot_foreach_cb,
        (functions, ui.tree_plot.get_selection()))
    
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
