# pyprop.py
#
#  For easy creation of python properties
#  Author: Runsun Pan
#
#  This function was coded in 2009 with python 2.5.2 
#  and publiched in ActiveState Code Recipes:
# http://code.activestate.com/recipes/576742-easy-property-creation-in-python/
# http://www.sourcecodeonline.com/details/easy_property_creation_in_python.html
#  It still works in python 3.7

import inspect 

def prop(func):
    '''A decorator function for easy property creation.

    Turn a func into a property. 

    @prop
    def myprop(self, arg1, ...): 
    return { 'fset': lambda ...  
           , 'fget': lambda ... 
           , 'fdel': lambda ... 
           , 'doc': <string>    
           , 'prefix': ""       
           }

    The example above turns *myprop* into a property, with 
    internal var name = 'myprop', like self.myprop

    If prefix (say, "_"), internal name = "_myprop": self._myprop

    If fset = None: read-only (you canNOT set value) 


    >>> class CLS(object):
    ...   def __init__(self):
    ...      self._name='Runsun Pan'
    ...      self._mod='panprop'
    ...      self._height= 54
    ...      self.CLS_crazy = 'Customized internal name'
    ...
    ...   @prop
    ...   def name(self): pass           # Normal property, Simply pass
    ...
    ...   @prop
    ...   def mod(self):                 # Read-only, customized get
    ...      return {'fset':None,
    ...              'fget': lambda self: "{%s}"%self._mod  }
    ...
    ...   @prop
    ...   def height(self, h):           # Read and set
    ...      return {'fset':lambda self,h: setattr(self,'_height',h),
    ...              'fget': lambda self: self._height  }
    ...
    ...   @prop
    ...   def undead(self):             # undead
    ...      return {'fget':lambda self: "Undead property",
    ...              'fdel': None  
    ...             }
    ...
    ...   @prop
    ...   def crazy(self):               # Doc string and customized prefix
    ...      return {'prefix': 'CLS_',
    ...              'doc':'I can be customized!'}

    >>> cls = CLS()

    ----------------------------   default
    >>> cls.name
    'Runsun Pan'

    >>> cls.name = "Pan"
    >>> cls.name
    'Pan'

    ---------------------------   Read-only
    >>> cls.mod
    '{panprop}'

    Trying to set cls.mod=??? will get:
    AttributeError: can't set attribute 

    ---------------------------   Read and set
    >>> cls.height
    54
    >>> cls.height= 70
    >>> cls.height
    70
    
    ---------------------------   undead
    >>> cls.undead
    'Undead property'

    >> del cls.undead  # Cause AttributeError: can't delete attribute
    
    ---------------------------   Customized prefix for internal name
    >>> cls.crazy       
    'Customized internal name'

    >>> cls.CLS_crazy
    'Customized internal name'

    ---------------------------   docstring 
    >>> CLS.name.__doc__
    ''
    
    >>> CLS.mod.__doc__
    ''
    
    >>> CLS.crazy.__doc__
    'I can be customized!'

    ---------------------------  delete
    >>> del cls.crazy

    Trying to get cls.crazy will get:
    AttributeError: 'CLS' object has no attribute 'CLS_crazy'



      
    '''
    
    
    ## 2020.9.9
    ## Add args_to_func below to deliver the arguments given to func. 
    ## The following 2 lines replaced the line "ops = func() or {}""
    args_to_func = inspect.signature(func)._parameters 
    ops = func( **args_to_func ) or {}
    
    name=ops.get('prefix','_')+func.__name__ # property name
    fget=ops.get('fget',lambda self:getattr(self, name))
    fset=ops.get('fset',lambda self,value:setattr(self,name,value))
    fdel=ops.get('fdel',lambda self:delattr(self,name))
    return property ( fget, fset, fdel, ops.get('doc','') )

def test():   
    import doctest 
    print('--- Using README.md file for doctest:')
    doc = ''.join( open('README.md', 'r').readlines() )
    prop.__doc__ = doc
    doctest.testmod()  
    print('--- Tests done.')

if __name__=='__main__':
    
    print('*** Doctesting  ***')
    import doctest
    doctest.testmod(verbose = False)
    print('*** Done ***')
    #doctest.run_docstring_examples(get_rng_by_rel_rng, globals())
    #print(tl.text())
    #re_test()
    #print("\n\n")



""" readme.md

# A function *prop()* for Easy Property Creation in Python 

Presented in this recipe is a function **prop()**, with that a property 
**myprop** can be created as simple as:

``` python
@prop
def myprop(): 
   return { 'fset': lambda ...  
          , 'fget': lambda ... 
          , 'fdel': lambda ... 
          , 'doc': <string>          
          }
```          

All the items in the returned dict are optional. 

The function contains only 7 lines of code, easy to understand, easy to 
customize, will make the code look much netter and will save you a lot 
of typing.

## Background

This code was written in 2009 in python 2.5.2, and published in ActiveState 
Code Recipes:
http://code.activestate.com/recipes/576742-easy-property-creation-in-python/

It still works well as of today (python 3.7).

The standard procedure for creating properties for a class in python is 
quite tedious. We have to do this using the built-in function property:

``` python
class C(object):
    def __init__(self): 
        self._x = None
    def getx(self): return self._x
    def setx(self, value): self._x = value
    def delx(self): del self._x
    x = property(getx, setx, delx, "I'm the 'x' property.")
```

That is, creating a single property - even the property is as simple as 
retrieving or setting an internal variable - requires 1 to 3 property-behavior 
functions (getx, setx, delx) that are not intended for users access but flood 
the class instance namespace.

The better way of creating properties would have fit the requirements: 
(1) No flooding in the instance namespace; 
(2) Simple usage for basic properties; 
(3) Customizable for complicated properties.

A good solution making use of the decorator is provided by Walker Hale 
in a comment to a recipe http://code.activestate.com/recipes/410698/ :

``` python
def newProp( fcn ):
    return property( **fcn() )

class Example(object):

    @newProp
    def myattr():
        doc = "This is the doc string."

        def fget(self):
            return self._value

        def fset(self, value):
            self._value = value

        def fdel(self):
            del self._value

        return locals()
```

It moves the *property-behavior* functions from the class instance 
namespace to the *locals()* namespace of a function, which is returned 
to a decorator *newProp* that uses it to execute and return the result 
of the built-in property function.

The problem of *namespace flooding* is solved. But it still requires 
tedious input of functions for every single simple property.

### My solution

I asked the question: Why not just transfer the burden of defining 
these *property-behavior functions to the decorator ?*

That's what I present here. In short, it instructs the decorator to 
take charge of defining *property-behavior*, so users don't have to 
type in tedious code for every property. Thus, creating simple, 
bare-bone properties can't be easier:

``` python
class MyCls(object):
    def __init__(self):
        self._p1=0
        self._p2='test'
        self._p3=[]

    @prop
    def p1(self):pass

    @prop
    def p2(self):pass

    @prop
    def p3(self):pass
```

Every property of name X assumes that the internal variable to store 
its value is _X, which can be customized. See the example *CLS_crazy* 
in docstring.

More complicated properties can be created by returning a dict (instead 
of just pass):

### Customized behavior functions

``` python
@prop
def count(): 
    return {'fget':lambda self: self.start+self._count}

@prop
def aName():
    return {'fset':lambda self,v: self._aName= 'Dr. '+aName }
```

### Read-only:

``` python
@prop
def reader(): return {'fset':None}
```

### Undead:

``` python
@prop
def reader(): return {'fdel':None}
```

### Define docstring:

``` python
@prop
def documented(): 
    return {'doc': 'A documented property'}
```

"""    