import math
import time
import cairo

import plotter

def Property(fn):
    return property(**fn())

class Graph(object):
    """ A paintboard for graphing that will get transfered to a
    destination surface when the drawing is complete """
    
    def __init__(self, size, resolution):
        """ Initialize the canvas instance
        
        Named Arguments:
        * size -- A list containing the width and height of the
          target surface. Format: (width, height)
        * resolution -- A list containing the window of the graph
          that will be drawn. Format: (x_min, x_max, y_min, y_max)
        
        """
        
        self.size = list(size)
        self.resolution = list(resolution)
    
    def render(self, functions, trace=None):
        origin_x, origin_y = self.canvas_point(0,0)
        
        # Set-up canvas and context
        canvas = cairo.ImageSurface(cairo.FORMAT_ARGB32,
            self.width, self.height)
        cr = cairo.Context(canvas)
        
        # Prepare Labeling
        extents = dict(zip(["ascent", "descent", "height", "max_x_advance", "max_y_advance"],
            cr.font_extents()))
        
        # Profiling
        #total = time.time()
        
        # Blank canvas
        cr.set_source_rgb(1.0,1.0,1.0)
        cr.rectangle(0, 0, self.width, self.height)
        cr.fill()
        
        # Drawing Coordinate Plane
        cr.set_source_rgb(0,0,0)
        cr.set_line_width(1)
        
        # X axis
        cr.move_to(0, origin_y)
        cr.line_to(self.width, origin_y)
        
        #Y axis
        cr.move_to(origin_x, 0)
        cr.line_to(origin_x, self.height)
        
        # Major ticks
        for i in plotter.marks(self.xmin, self.xmax):
            if i != 0:
                cr.move_to(self.canvas_x(i), origin_y - 5)
                cr.line_to(self.canvas_x(i), origin_y + 5)
                
                cr.move_to(self.canvas_x(i), origin_y + extents['height'])
                cr.show_text(str(i))
        
        for i in plotter.marks(self.ymin, self.ymax):
            if i != 0:
                cr.move_to(origin_x - 5, self.canvas_y(i))
                cr.line_to(origin_x + 5, self.canvas_y(i))
                
                c_y = self.canvas_y(i)
                c_y = c_y + extents['height'] if i > 0 else c_y
                cr.move_to(origin_x + 7.5, c_y)
                cr.show_text(str(i))
        
        # Minor ticks
        for i in plotter.marks(self.xmin, self.xmax, 10):
            if i != 0:
                cr.move_to(self.canvas_x(i), origin_y - 2.5)
                cr.line_to(self.canvas_x(i), origin_y + 2.5)
        
        for i in plotter.marks(self.xmin, self.xmax, 10):
            if i != 0:
                cr.move_to(origin_x - 2.5, self.canvas_y(i))
                cr.line_to(origin_x + 2.5, self.canvas_y(i))
        
        cr.stroke()
        
        plot_start = time.time()
        
        # Function Plotting
        if len(functions) > 0:
            for function in functions:
                prev_drawn = False
                
                for point in function.plot(self.domain()):
                    x, y = point
                    
                    canvas_x = self.canvas_x(x)
                    canvas_y = self.canvas_y(y) if y is not None else None
                    
                    if canvas_y is not None and \
                        canvas_y > 0 and canvas_y < self.height:
                        
                        if prev_drawn:
                            cr.line_to(canvas_x, canvas_y)
                        else:
                            cr.move_to(canvas_x, canvas_y)
                            prev_drawn = True
                        
                    else: prev_drawn = False
                
                r, g, b, a = function.color
                cr.set_source_rgb(r, g, b)
                cr.set_line_width(3 if function.highlight else 1)
                cr.stroke()
        
        #print "functions:", (time.time() - plot_start) * 1000
        
        #trace_start = time.time()
        
        if trace is not None:
            canvas_x = self.canvas_x(trace)
            
            cr.set_source_rgb(1, 0, 0)
            cr.set_line_width(1)
            cr.move_to(canvas_x, 0)
            cr.line_to(canvas_x, self.height)
            cr.stroke()
            
            for function in functions:
                x, y = function.evaluate(trace)
                
                canvas_y = self.canvas_y(y) if y is not None else -1
                
                if canvas_y > 0 and canvas_y < self.height:
                    cr.set_source_rgb(1,0,0)
                    cr.set_line_width(1)
                    cr.move_to(canvas_x - 5, canvas_y - 5)
                    cr.line_to(canvas_x + 5, canvas_y + 5)
                    cr.move_to(canvas_x + 5, canvas_y - 5)
                    cr.line_to(canvas_x - 5, canvas_y + 5)
                    cr.stroke()
                    
                    c_y = self.canvas_y(y)
                    c_y = c_y + extents['height'] if y > 0 else c_y
                    cr.move_to(canvas_x + 7.5, c_y)
                    cr.text_path("(%0.2f, %0.2f)" % (x, y))
                    cr.set_source_rgba(1,1,1,0.5)
                    cr.set_line_width(6)
                    cr.stroke_preserve()
                    cr.set_source_rgb(0,0,0)
                    cr.fill()
        
        #print "Trace:", (time.time() - trace_start) * 1000
        
        #print "Total:", (time.time() - total) * 1000
        
        return canvas
    
    def domain(self):
        """ Generator for the domain allowed by the window
        
        Preserves the memory saving feature of xrange by avoiding
        mapping it to Graph.graph_x (which creates a list,) and
        maintaining the simplicity of already having graphing space
        coords to work with.
        
        """
        
        domain = xrange(0, self.width, 1)
        
        for x in domain:
            yield self.graph_x(x)
    
    @Property
    def width():
        def fget(self):
            return self.size[0]
        
        def fset(self, width):
            self.size[0] = width
        
        return locals()
    
    @Property
    def height():
        def fget(self):
            return self.size[1]
        
        def fset(self, height):
            self.size[1] = height
        
        return locals()
    
    @Property
    def xmin():
        def fget(self):
            return self.resolution[0]
        
        def fset(self, xmin):
            self.resolution[0] = xmin
        
        return locals()
    
    @Property
    def xmax():
        def fget(self):
            return self.resolution[1]
        
        def fset(self, xmax):
            self.resolution[1] = xmax
        
        return locals()
    
    @Property
    def ymin():
        def fget(self):
            return self.resolution[2]
        
        def fset(self, ymin):
            self.resolution[2] = ymin
        
        return locals()
    
    @Property
    def ymax():
        def fget(self):
            return self.resolution[3]
        
        def fset(self, ymax):
            self.resolution[3] = ymax
        
        return locals()
    
    def canvas_x(self, x):
        """ Converts an x value from canvas space to graph space
        
        """
        
        return int(round((x - self.xmin) * self.width / (self.xmax - self.xmin)))
    
    def canvas_y(self, y):
        """ Converts a y value from canvas space to graph space
        
        """
        
        return int(round((self.ymax - y) * self.height / (self.ymax - self.ymin)))
    
    def canvas_point(self, x, y):
        """ Converts a point from canvas space to graph space
        
        """
        
        return (self.canvas_x(x), self.canvas_y(y))
    
    def graph_x(self, x):
        """ Converts an x value from graph space to canvas space
        
        """
        
        return x * (self.xmax - self.xmin) / float(self.width) + self.xmin
    
    def graph_y(self, y):
        """ Converts a y value from graph space to canvas space
        
        """
        
        return self.ymax - (y * (self.ymax - self.ymin) / float(self.height))
    
    def graph_point(self, x, y):
        """ Converts point from graph space to canvas space
        
        """
        
        return (self.graph_x(x), self.graph_y(y))

