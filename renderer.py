import plotter

class Canvas(object):
    def __init__(self, width, height, resolution):
        self.width = width
        self.height = heigth
        self.xmin, self.xmax, self.ymin, self.ymax = resolution
    
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

def render_all(surface):
    pass

def render_marks(surface):
    pass

def render_plots(surface):
    pass


