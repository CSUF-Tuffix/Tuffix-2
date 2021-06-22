import pkgutil
import re
import sys
import inspect

_re = re.compile('test_.*|[a-zA-Z]+.*Test', re.IGNORECASE)

"""
example matches:

LSBTest
test_constructor
"""
global current_namespace
global current_childname

# current_namespace, current_childname = None, None

__unit_test_hierarchy__ = {}

# get the UnitTest library layout

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    if(_re.match(module_name) and module_name not in __unit_test_hierarchy__):

        # activate the module
        _module = loader.find_module(module_name).load_module(module_name)
        globals()[module_name] = _module

        # https://stackoverflow.com/questions/1796180/how-can-i-get-a-list-of-all-classes-within-current-module-in-python
        for _class in inspect.getmembers(
                sys.modules[module_name], inspect.isclass):
            name, _ = _class
            if(_re.match(name)):
                __unit_test_hierarchy__[module_name] = name

"""
# this body works for sure
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    if(_re.match(module_name)):
        __all__.append(module_name)
        _module = loader.find_module(module_name).load_module(module_name)
        globals()[module_name] = _module
"""
