from functools import wraps
from .flag import *

__hook_exclude_name = (
    "dir", "dirxml", "profile", "profileEnd", "clear", "table", "keys", "values",
    "debug", "undebug", "inspect", "copy", "queryObjects", 'monitor', 'unmonitor',
    "$", "$$", "$_", "$0", "$1", "$2", "$3", "$4", "$", "$x", "DataVie",
    "String", "Array", "Date", "Object", "window", "Symbol", "Number", "Function",
    "Symbol.toPrimitive", "Symbol.toStringTag",
    "parseFloat", "parseInt", "Math", "BigInt", "RegExp", "console", "isNaN", "Boolean",
    "faker",  "unescape", "NaN", "Infinity", "_cf_chl_opt", "decodeURIComponent"
)


def __v8_get_hook__(self, name, value=None, error=None, ctx_type=''):
    if name in __hook_exclude_name:
        return
    if isinstance(name, str) and name.startswith('a1_0x'):
        return
    msg = f"{ctx_type} getter: {self.__class__.__name__}.{name} -> {value}"
    if error:
        msg += f", error: {error}"
    print(msg)


def __v8_set_hook__(self, name, value, error, ctx_type=''):
    if isinstance(name, str) and name.startswith('a1_0x'):
        return
    msg = f"{ctx_type} setter: {self.__class__.__name__}.{name} = {value}"
    if error:
        msg += f", error: {error}"
    print(msg)


def __v8_method_hook__(self, func_name, arguments, value, has_error, ctx_type=''):
    msg = f"{ctx_type} method: {self.__name__ if isinstance(self, type) else self.__class__.__name__}.{func_name}{tuple(arguments)}"
    if has_error:
        msg += f" -> error: {value}"
    else:
        msg += f" -> {value}"
    print(msg)


def __v8_construct_hook__(name, arguments, value, has_error, is_construct_call, ctx_type=''):
    if is_construct_call:
        msg = f"{ctx_type} construct: new {name}{tuple(arguments)} -> {value}"
    else:
        msg = f"{ctx_type} construct: {name}{tuple(arguments)} -> {value}"
    if has_error:
        msg += f", has_error: {has_error}"
    print(msg)

exposed_constructs = {}

class ConstructorConfig:
    def __init__(
            self,
            exposed=FlagExposed.kYes,
            constructor=FlagConstructor.kDontAll,
            length=0,
            v8_array=0,  # FlagArrayProto
            immutable=0,
            has_constructor=1,
            hook=True,
    ):
        self.exposed = exposed
        self.constructor = constructor
        self.length = length
        self.hook = hook
        self.v8_array = v8_array
        self.immutable = immutable
        self.has_constructor = has_constructor

    def __call__(self, cls):
        if self.exposed == FlagExposed.kYes:
            exposed_constructs[cls.__name__] = cls
        setattr(cls, "__v8_constructor__", self.constructor)
        setattr(cls, "__v8_length__", self.length)
        setattr(cls, "__v8_array__", self.v8_array)
        setattr(cls, "__v8_immutable__", self.immutable)
        setattr(cls, "__v8_has_constructor__", self.has_constructor)
        if self.hook:
            cls.__v8_get_hook__ = __v8_get_hook__
            cls.__v8_set_hook__ = __v8_set_hook__
            cls.__v8_method_hook__ = __v8_method_hook__
            cls.__v8_construct_hook__ = __v8_construct_hook__
        return cls

    def __str__(self):
        return f'construct_{self.exposed}{self.constructor}{self.length}{int(self.v8_array)}{int(self.immutable)}{int(self.has_constructor)}'


def impl_warp(cls):
    father = cls.__base__
    for name in cls.__dict__:
        if name == '__module__':
            continue
        setattr(father, name, cls.__dict__[name])
    return father


def attr_warp(**attrs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        for name, value in attrs.items():
            setattr(wrapper, name, value)
        return wrapper
    return decorator


class CtxTypeIndex:
    count = 0

    @classmethod
    def get(cls):
        cls.count += 1
        return cls.count
