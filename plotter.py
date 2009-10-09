from math import *

__all__ = ['safe_dict']

# I knew this app was going to borrow  heavily from Lybniz, but this
# is going to get ridiculous... I'm going to have to figure everything
# out before I can pull it apart and get it back together again.

# Anyway, this next block of code is from Lybniz

# some extra maths functions
fac = factorial

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

# End Lybniz

def precompile_plot(model, path, row_iter, plots):
    if model[path][1]: function = model[path][0].replace("^","**")
    else: function = ""
    
    if function != "":
        try:
            compiled = compile(function,"",'eval')
            c = hashlib.md5(function).hexdigest()
            r = float(int(c[0:10],  16)) / 16**10
            g = float(int(c[10:20], 16)) / 16**10
            b = float(int(c[20:30], 16)) / 16**10
            plots.append((compiled, (r, g, b)))
            model[path][2] = None
        except SyntaxError:
            model[path][2] = gtk.icon_theme_get_default().load_icon(
                "gtk-dialog-warning", gtk.ICON_SIZE_MENU, 0)

def plot(fn, x):
    """ Generator """
    
    pass

def trace():
    pass


