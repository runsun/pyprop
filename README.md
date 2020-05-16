# pyprop for Easy Property Creation in Python 

Presented in this recipe is a function **prop**, with that a property **myprop** can be created as simple as:

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

The function contains only 7 lines of code, easy to understand, easy to customize, will make the code look much netter and will save you a lot of typing.

## Background

This code was written in 2009 in python 2.5.2, and published in ActiveState Code Recipes:
http://code.activestate.com/recipes/576742-easy-property-creation-in-python/

The standard procedure for creating properties for a class in python is quite tedious. We have to do this using the built-in function property:

``` python
class C(object):
    def __init__(self): 
        self._x = None
    def getx(self): return self._x
    def setx(self, value): self._x = value
    def delx(self): del self._x
    x = property(getx, setx, delx, "I'm the 'x' property.")
```

That is, creating a single property - even the property is as simple as retrieving or setting an internal variable - requires 1 to 3 property-behavior functions (getx, setx, delx) that are not intended for users access but flood the class instance namespace.

The better way of creating properties would have fit the requirements: (1) No flooding in the instance namespace; (2) Simple usage for basic properties; (3) Customizable for complicated properties.

A good solution making use of the decorator is provided by Walker Hale in a comment to a recipe http://code.activestate.com/recipes/410698/ :

``` python
def newProp( fcn ):
    return property( **fcn() )

class Example(object):

    @newProp
    def myattr():
        doc = """This is the doc string."""

        def fget(self):
            return self._value

        def fset(self, value):
            self._value = value

        def fdel(self):
            del self._value

        return locals()
```

It moves the *property-behavior* functions from the class instance namespace to the *locals()* namespace of a function, which is returned to a decorator *newProp* that uses it to execute and return the result of the built-in property function.

The problem of *namespace flooding* is solved. But it still requires tedious input of functions for every single simple property.

### My solution

I asked the question: Why not just transfer the burden of defining these *property-behavior functions to the decorator ?*

That's what I present here. In short, it instructs the decorator to take charge of defining *property-behavior*, so users don't have to type in tedious code for every property. Thus, creating simple, bare-bone properties can't be easier:

``` python
class MyCls(object):
    def __init__(self):
        self._p1=0
        self._p2='test'
        self._p3=[]

    @prop
    def p1():pass

    @prop
    def p2():pass

    @prop
    def p3():pass
```

Every property of name X assumes that the internal variable to store its value is _X, which can be customized. See the example *CLS_crazy* in docstring.

More complicated properties can be created by returning a dict (instead of just pass):

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

