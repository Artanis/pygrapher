# -*- coding: UTF-8 -*-

import hashlib
from math import *

__all__ = ['Function']

# I knew this app was going to borrow  heavily from Lybniz, but this
# is going to get ridiculous... I'm going to have to figure everything
# out before I can pull it apart and get it back together again.

# Anyway, this next block of code is from Lybniz. I've made a few
# changes, though. Formatting, comments, avoiding re-inventing the
# wheel, etc.
#
# Text of the Lybniz COPYING file, just in case (seems like overkill
# for just a few functions, though...):
#
# =====================================================================
# Copyright (c) 2005-2006, Thomas Führinger, Sam Tygier
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of the Lybniz dev team nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# =====================================================================

# some extra maths functions
# Note: turns out factorial is defined in the math module. No need
# to re-invent, so we'll just grab a reference to it for use in the
# dictionary.
fac = factorial

def sinc(x):
    if x == 0:
        return 1
    return sin(x)/x

# create a safe namespace for the eval()s in the graph drawing code
def sub_dict(somedict, somekeys, default=None):
    """ Filters a dict against a list of keys.
    
    Named Arguments:
    * somedict -- a dictionary
    * somekeys -- a list of strings used to filter the keys in somedict
    * default -- the default value keys in somekeys but not in somedict
      should take in the returned dict. Defaults to None.
    
    """
    
    return dict([(k, somedict.get(k, default)) for k in somekeys])

# a list of the functions from math that we want.
safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos',
    'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp',
    'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians',
    'sin', 'sinh', 'sqrt', 'tan', 'tanh','fac', 'factorial', 'sinc']

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

    a = a + log10(minor)

    width = max_val - min_val
    log10_range = log10(width)

    interval = 10 ** int(floor(log10_range - a))
    lower_mark = min_val - fmod(min_val,interval)
    
    if lower_mark < min_val:
        lower_mark += interval

    a_mark = lower_mark
    while a_mark <= max_val:
        if abs(a_mark) < interval / 2:
            a_mark = 0
        yield a_mark
        a_mark += interval

# End Lybniz

class Function(object):
    """ Defines a function of x and provides methods to evaluate that
    function at any value of x, and to plot it against a domain.
    
    Well, it's *intended* to represent f(x), but you can force f(y) by
    swapping the range with the domain and swapping the x and y values
    provided by the evaluation functions.
    
    For example, normally you'd use:
    
        x, y = f_of_x.evaluate(x)
    
    But you could also use:
    
        y, x = f_of_y.evaluate(y)
    
    """
    
    def __init__(self, function_definition, active=True, highlight=False):
        self.__function = function_definition
        self.active = active
        self.highlight = highlight
    
    @property
    def color(self):
        """ A tuple containing the color of this function in RGBA space,
        where the individual components are in the set of Rational
        numbers between 0.0 and 1.0 inclusive.
        
        Generated automatically from the text of the function via MD5
        hash, with each components taking 8 digits of the hexdigest
        each. From RGB, the highest and lowest values are selected and
        made 1.0 and 0.0 respectively, the other is scaled to that
        range. Alpha is divided by it's maximum possible value.
        
        """
        
        color = hashlib.md5(self.__function).hexdigest()
        color = [int(color[0:8], 16), int(color[8:16], 16),
            int(color[16:24], 16), int(color[24:32], 16)]
        
        top = float(max(color[0:3]))
        bottom = float(min(color[0:3]))
        
        return ((color[0]-bottom) / (top-bottom), (color[1]-bottom) / (top-bottom),
            (color[2]-bottom) / (top-bottom), color[3] / float(16**8))
    
    def __repr__(self):
        return """Function("%s", active=%s, highlight=%s)""" % (
            self.__function, self.active, self.highlight)
    
    def __str__(self):
        return """f(x) = %s""" % self.__function
    
    def __compile(self):
        """ Compiles the function text """
        try:
            return compile(self.__function, "", "eval")
        except SyntaxError: 
            print "Syntax Error:", self.function
        except TypeError:
            print "Type Error: null bytes in source", 
    
    def plot(self, domain):
        """ Generate coordinates for each real number provided in domain
        
        Named Arguments:
        * domain -- a (finite) list of real numbers. Sorry, but
          calculating values for domains of infinite size is just too
          much work.
        
        Returns a generator for the coordinates, which provides points
        as tuple(x_value, y_value).
        
        """
        function = self.__compile()
        
        namespace = safe_dict.copy()
        
        for x in domain:
            yield self.evaluate(x, function, namespace)
    
    def evaluate(self, x, function=None, namespace=None):
        """ Return coordinate for the given x value
        
        Named Arguments:
        * x -- value to evaluate the function at
        * function -- pre-compiled function ready for evaluation. Leave
          default to have this method compile the function.
        * namespace -- pre-existing namespace definition for safe
          evaluation. Leave default to have this method create a safe
          namespace from the safe_dict module variable.
        
        The function and namespace parameters exist mostly for use with
        the plot method. It is highly recommended to allow this method
        to construct those two parameters under most circumstances.
        
        Returns a tuple containing the point as tuple(x_value, y_value).
        
        """
        
        function = self.__compile() if function is None else function
        
        namespace = safe_dict.copy() if namespace is None else namespace
        
        namespace['x'] = x
        
        y = None
        try: y = eval(function, {'__builtins__':{}}, namespace)
        except: pass
        
        return (x, y)

