import plotter

class Canvas(object):
    """ A paintboard that will get transfered to a destination surface
    when the drawing is complete """
    
    def __init__(self, size, resolution):
        """ Initialize the canvas instance
        
        Named Arguments:
        * size -- An iterable containing the width and height of the
          target surface. Format: (width, height)
        * resolution -- An interable containing the window of the graph
          that will be drawn. Format: (x_min, x_max, y_min, y_max)
        
        """
        
        self.size = list(size)
        self.resolution = list(resolution)
    
    @property
    def width():
        def fget(self):
            return self.size[0]
        
        def fset(self, width):
            self.size[0] = width
        
        return locals()
    
    @property
    def height():
        def fget(self):
            return self.size[1]
        
        def fset(self, height):
            self.size[1] = height
        
        return locals()
    
    @property
    def xmin():
        def fget(self):
            return self.resolution[0]
        
        def fset(self, xmin):
            self.resolution[0] = xmin
        
        return locals()
    
    @property
    def xmax():
        def fget(self):
            return self.resolution[1]
        
        def fset(self, xmax):
            self.resolution[1] = xmax
        
        return locals()
    
    @property
    def ymin():
        def fget(self):
            return self.resolution[2]
        
        def fset(self, ymin):
            self.resolution[2] = ymin
        
        return locals()
    
    @property
    def ymax():
        def fget(self):
            return self.resolution[3]
        
        def fset(self, ymax):
            self.resolution[3] = ymax
        
        return locals()
    
    def canvas_x(self, x):
        """ Converts an x value from canvas space to graph space
        
        Named Arguments:
        * x -- The x value to convert
        
        """
        
        return (x - self.xmin) * self.width / (self.xmax - self.xmin)
    
    def canvas_y(self, y):
        """ Converts a y value from canvas space to graph space
                
        Named Arguments:
        * y -- The y value to convert
        
        """
        
        return (self.ymax - y) * self.height / (self.ymax - self.ymin)
    
    def canvas_point(self, point):
        """ Converts a point from canvas space to graph space
        
        Named Arguments:
        * point -- A tuple containing x and y values in canvas space
        
        """
        
        x, y = point
        return (self.canvas_x(x), self.canvas_y(y))
    
    def graph_x(self, x):
        """ Converts an x value from graph space to canvas space
                
        Named Arguments:
        * x -- The x value to convert
        
        """
        
        return x * (self.xmax - self.xmin) / self.width + self.xmin
    
    def graph_y(self, y):
        """ Converts a y value from graph space to canvas space
                
        Named Arguments:
        * y -- The y value to convert
        
        """
        
        return self.ymax - (y * (self.ymax - self.ymin) / self.height)
    
    def graph_point(self, point):
        """ Converts point from graph space to canvas space
                
        Named Arguments:
        * point -- A tuple containing x and y values in graph space
        
        """
        
        x, y = point
        return (self.graph_x(x), self.graph_y(y))

