# -*- coding: UTF-8 -*-

import gtk
import math
from math import *
from time import time
import hashlib

import ui
import plotter
import renderer

# I knew this app was going to borrow  heavily from Lybniz, but this
# is going to get ridiculous... I'm going to have to figure everything
# out before I can pull it apart and get it back together again.

# Anyway, this next block of code is from Lybniz

# some extra maths functions
def fac(x):
	if type(x) != int or x < 0:
		raise ValueError
	if x==0:
		return 1
	for n in range(2,x):
		x = x*n
	return x

def sinc(x):
	if x == 0:
		return 1
	return sin(x)/x

# create a safe namespace for the eval()s in the graph drawing code
def sub_dict(somedict, somekeys, default=None):
	return dict([ (k, somedict.get(k, default)) for k in somekeys ])
# a list of the functions from math that we want.
safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh','fac','sinc']
safe_dict = sub_dict(locals(), safe_list)

# End Lybniz

def expose_graph (draw, event):
    # Profiling
    draw_start = time()
    
    x, y, w, h = draw.get_allocation()
    cr = draw.window.cairo_create()
    
    # Prepare Canvas
    cr.set_source_rgb(1.0,1.0,1.0)
    cr.rectangle(0,0,w,h)
    cr.fill()    
    
    # Prepare canvas <=> graph translations
    xmin, xmax, ymin, ymax = ui.resolution()
    canvas_x = lambda x: (x - xmin) * w / (xmax - xmin)
    canvas_y = lambda y: (ymax - y) * h / (ymax - ymin)
    canvas_point = lambda x,y: (canvas_x(x), canvas_y(y))
    graph_x = lambda x: x * (xmax - xmin) / w + xmin
    graph_y = lambda y: ymax - (y * (ymax - ymin) / h)
    
    origin_x = int(round(canvas_x(0)))
    origin_y = int(round(canvas_y(0)))
    
    # Draw Coordinate Plane
    factor = 1
    
    # Draw cross
    # Y axis
    cr.set_source_rgb(0,0,0)
    cr.move_to(origin_x, 0)
    cr.line_to(origin_x, h)
    cr.set_line_width(1.5)
    cr.stroke()
    # X axis
    cr.set_source_rgb(0,0,0)
    cr.move_to(0, origin_y)
    cr.line_to(w, origin_y)
    cr.set_line_width(1.5)
    cr.stroke()
    
    for i in plotter.marks(xmin / factor, xmax / factor):
        label = '%g' % i if i != 0 else ""
        i = i * factor
        
        cr.set_source_rgb(0,0,0)
        cr.move_to(int(round(canvas_x(i))), origin_y - 5)
        cr.line_to(int(round(canvas_x(i))), origin_y + 5)
        cr.set_line_width(1)
        cr.stroke()
        
        cr.set_source_rgb(0,0,0)
        cr.move_to(int(round(canvas_x(i))) + -5 , origin_y + 15)
        cr.text_path(label)
        cr.fill()
    
    for i in plotter.marks(ymin, ymax):
        label = '%g' % i if i != 0 else ""
        
        cr.set_source_rgb(0,0,0)
        cr.move_to(origin_x - 5, int(round(canvas_y(i))))
        cr.line_to(origin_x + 5, int(round(canvas_y(i))))
        cr.set_line_width(1)
        cr.stroke()
        
        cr.set_source_rgb(0,0,0)
        cr.move_to(origin_x - 15, int(round(canvas_y(i))) + 5)
        cr.text_path(label)
        cr.fill()
    
    for i in plotter.marks(xmin / factor, xmax / factor, minor=10):
        i = i * factor
        
        cr.set_source_rgb(0,0,0)
        cr.move_to(int(round(canvas_x(i))), origin_y - 2)
        cr.line_to(int(round(canvas_x(i))), origin_y + 2)
        cr.set_line_width(1)
        cr.stroke()
    
    for i in plotter.marks(ymin, ymax, minor=10):
        cr.set_source_rgb(0,0,0)
        cr.move_to(origin_x - 2, int(round(canvas_y(i))))
        cr.line_to(origin_x + 2, int(round(canvas_y(i))))
        cr.set_line_width(1)
        cr.stroke()
    
    # Plot graphs
    functions = []
    def foreach_cb(treemodel, treepath, treeiter):
        if treemodel[treepath][1] and treemodel[treepath][0] != "":
            functions.append(plotter.Function(treemodel[treepath][0]))
    
    ui.store_plot.foreach(foreach_cb)
    
    if len(functions) > 0:
        domain = map(graph_x, xrange(0, w, 1))
        
        for function in functions:
            prev_drawn = False
            for point in function.plot(domain):
                p_x, p_y = point
                
                p_x = int(round(canvas_x(p_x)))
                
                p_y = int(round(canvas_y(p_y))) if p_y is not None else None
                
                if p_y is None or p_y < 0 or p_y > h:
                    prev_drawn = False
                else:
                    if prev_drawn:
                        cr.line_to(p_x, p_y)
                        prev_drawn = True
                    else:
                        cr.move_to(p_x, p_y)
                        prev_drawn = True
            
            r, g, b, a = function.color
            cr.set_source_rgb(r, g, b)
            cr.set_line_width(1)
            cr.stroke()
    
    # Draw the trace line and highlight intersections (with coords)
    b_trace, x_value = ui.trace()
    if b_trace:
        c_x = int(round(canvas_x(x_value)))
        
        cr.move_to(c_x, 0)
        cr.line_to(c_x, h)
        
        cr.set_source_rgb(1,0,0)
        cr.set_line_width(1)
        cr.stroke()
        
        for function in functions:
            x_value, y_value = function.evaluate(x_value)
            
            c_y = -1
            if y_value is not None:
                c_y = int(round(canvas_y(y_value)))
            
            if c_y > 0 and c_y < h:
                cr.set_source_rgb(1,0,0)
                cr.set_line_width(1)
                cr.move_to(c_x - 5, c_y - 5)
                cr.line_to(c_x + 5, c_y + 5)
                cr.move_to(c_x + 5, c_y - 5)
                cr.line_to(c_x - 5, c_y + 5)
                cr.stroke()
                
                label = "(%0.4f, %0.4f)" % (x_value, y_value)
                cr.move_to(c_x+10, c_y+10)
                cr.text_path(label)
                cr.set_source_rgba(1,1,1,0.75)
                cr.set_line_width(6)
                cr.stroke_preserve()
                cr.set_source_rgb(0,0,0)
                cr.fill()
    
    draw_time = time() - draw_start
    cr.set_source_rgba(1,0,0,1)
    cr.move_to(10,h-10)
    cr.text_path(
        "(%d x %d; %4f) %fms" % (w, h, w/float(h), draw_time * 1000))
    cr.fill()

def refresh_graph(btn):
    expose_graph(ui.draw_graph, None)

ui.ui_tree.get_widget("btn_refresh").connect("clicked", refresh_graph)
ui.draw_graph.connect("expose-event", expose_graph)

ui.window_main.show_all()
gtk.main()
