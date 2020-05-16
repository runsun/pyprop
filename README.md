# pyprop for Easy Property Creation in Python 

Presented in this recipe is a function prop, with that a property myprop can be created as simple as:

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


