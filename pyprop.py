# pyprop.py
#
#  For easy creation of python properties
#  Author: Runsun Pan
#
#  This function was coded in 2009 with python 2.5.2 
#  and publiched in ActiveState Code Recipes:
# http://code.activestate.com/recipes/576742-easy-property-creation-in-python/
#
#  It still works in python 3.7


def prop(func):
    '''A decorator function for easy property creation.

        >>> class CLS(object):
        ...   def __init__(self):
        ...      self._name='Runsun Pan'
        ...      self._mod='panprop'
        ...      self.CLS_crazy = 'Customized internal name'
        ...
        ...   @prop
        ...   def name(): pass           # Simply pass
        ...
        ...   @prop
        ...   def mod():                 # Read-only, customized get
        ...      return {'fset':None,
        ...              'fget': lambda self: "{%s}"%self._mod  }
        ...
        ...   @prop
        ...   def crazy():               # Doc string and customized prefix
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
    ops = func() or {}
    name=ops.get('prefix','_')+func.__name__ # property name
    fget=ops.get('fget',lambda self:getattr(self, name))
    fset=ops.get('fset',lambda self,value:setattr(self,name,value))
    fdel=ops.get('fdel',lambda self:delattr(self,name))
    return property ( fget, fset, fdel, ops.get('doc','') )


if __name__=='__main__':
    
    print('*** Doctesting  ***')
    import doctest
    doctest.testmod(verbose = False)
    print('*** Done ***')
    #doctest.run_docstring_examples(get_rng_by_rel_rng, globals())
    #print(tl.text())
    #re_test()
    print("\n\n")