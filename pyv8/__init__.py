import os

from . import _pyv8
from .tools import *
from .flag import *

_pyv8.init_v8(
    icudtl_path=os.path.join(os.path.dirname(__file__), r'icudtl.dat'),
    params=[
        "--expose-gc",
        # "--no-freeze-flags-after-init",
        # "--max_old_space_size=4098",
        # "--max-shared-heap-size=4024",
        # "--max_semi_space_size=8096",
        # "--initial-shared-heap-size=4024",
        # "--single-threaded",
        # "--allow-natives-syntax"
        ]
)

Context = _pyv8.Context
Script = _pyv8.Script
Debugger = _pyv8.Debugger
JSObject = _pyv8.JSObject
JSPromise = _pyv8.JSPromise
JSTypeArray = _pyv8.JSTypeArray
JSFunction = _pyv8.JSFunction
JSException = _pyv8.JSException
JavaScriptTerminated = _pyv8.JavaScriptTerminated
Null = _pyv8.Null
Undefined = _pyv8.Undefined
current_context = _pyv8.current_context
new = _pyv8.new
v8_gc = _pyv8.v8_gc


from .devtools import start_devtools


class ArrayType:
    Uint32Array = 1
    Uint16Array = 2
    Uint8Array = 3
    Int32Array = 4
    Int16Array = 5
    Int8Array = 6
    Float64Array = 7
    Float32Array = 8
    Uint8ClampedArray = 9

