# -*- coding: UTF-8 -*-

import gtk
import math
from math import *
import hashlib

import ui

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

def precompile_plot(model, path, row_iter, plots):
    function = model[path][0].replace("^","**") if model[path][1] else ""
    
    if function != "":
        try:
            compiled = compile(function,"",'eval')
            c = hashlib.md5(function).hexdigest()
            r = float(int(c[0:10],  16)) / 16**10
            g = float(int(c[10:20], 16)) / 16**10
            b = float(int(c[20:30], 16)) / 16**10
            plots.append((compiled, (r, g, b)))
        except SyntaxError:
            print path[0], model[path][0]
            ui.status_main.push("Syntax Error: plot %3d - %s" % (path[0], model[path][0]))

def marks(min_val,max_val,minor=1):
	""" yield positions of scale marks between min and max. For making
	minor marks, set minor to the number of minors you want between
	majors
	
	Borrowed wholesale from Lybniz by Thomas Führinger and Sam Tygier
	
	Thanks guys!
	
	"""
	
	try:
		min_val = float(min_val)
		max_val = float(max_val)
	except:
		print "needs 2 numbers"
		raise ValueError

	if(min_val >= max_val):
		print "min bigger or equal to max"
		raise ValueError		

	a = 0.2 # tweakable control for when to switch scales
	          # big a value results in more marks

	a = a + math.log10(minor)

	width = max_val - min_val
	log10_range = math.log10(width)

	interval = 10 ** int(math.floor(log10_range - a))
	lower_mark = min_val - math.fmod(min_val,interval)
	
	if lower_mark < min_val:
		lower_mark += interval

	a_mark = lower_mark
	while a_mark <= max_val:
		if abs(a_mark) < interval / 2:
			a_mark = 0
		yield a_mark
		a_mark += interval

def expose_graph (draw, event):
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
    
    for i in marks(xmin / factor, xmax / factor):
        label = '%g' % i
        i = i * factor
        
        cr.set_source_rgb(0,0,0)
        cr.move_to(int(round(canvas_x(i))), origin_y - 5)
        cr.line_to(int(round(canvas_x(i))), origin_y + 5)
        cr.set_line_width(1)
        cr.stroke()
        
        cr.set_source_rgb(0,0,0)
        cr.move_to(int(round(canvas_x(i))) + 5 , origin_y + 10)
        cr.text_path(label)
        cr.fill()
    
    for i in marks(ymin, ymax):
        label = '%g' % i
        
        cr.set_source_rgb(0,0,0)
        cr.move_to(origin_x - 5, int(round(canvas_y(i))))
        cr.line_to(origin_x + 5, int(round(canvas_y(i))))
        cr.set_line_width(1)
        cr.stroke()
        
        cr.set_source_rgb(0,0,0)
        cr.move_to(origin_x + 5, int(round(canvas_y(i)))+10)
        cr.text_path(label)
        cr.fill()
    
    for i in marks(xmin / factor, xmax / factor, minor=10):
        i = i * factor
        
        cr.set_source_rgb(0,0,0)
        cr.move_to(int(round(canvas_x(i))), origin_y - 2)
        cr.line_to(int(round(canvas_x(i))), origin_y + 2)
        cr.set_line_width(1)
        cr.stroke()
    
    for i in marks(ymin, ymax, minor=10):
        cr.set_source_rgb(0,0,0)
        cr.move_to(origin_x - 2, int(round(canvas_y(i))))
        cr.line_to(origin_x + 2, int(round(canvas_y(i))))
        cr.set_line_width(1)
        cr.stroke()
    
    cr.set_source_rgba(1,0,0,0.25)
    cr.move_to(10,h-10)
    cr.text_path("(%d, %d)" % (w, h))
    cr.fill()
    
    # Plot graphs
    plots = []
    ui.store_plot.foreach(precompile_plot, plots)
    
    if len(plots) > 0:
        for i in xrange(0, w, 1):
            fnx = graph_x(i+1)
            prev = None
            for fn in plots:
                safe_dict['x'] = fnx
                fny = 0
                try:
                    fny = eval(fn[0],{'__builtins__':{}}, safe_dict)
                except:
                    prev = None
                    
                y_c = int(round(canvas_y(fny)))
                
                if y_c > 0 or y_c < h:
                    r, g, b = fn[1]
                    cr.set_source_rgb(r, g, b)
                    cr.arc(i, y_c, 2, 0, 2*math.pi)
                    cr.fill()
                    
                    prev = y_c

def refresh_graph(btn):
    expose_graph(ui.draw_graph, None)

ui.ui_tree.get_widget("btn_refresh").connect("clicked", refresh_graph)
ui.draw_graph.connect("expose-event", expose_graph)

ui.window_main.show_all()
gtk.main()
