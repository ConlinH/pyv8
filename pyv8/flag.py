from functools import wraps


class CallbackType:
    kPy = 0         # 回调Python类方法
    kJs = 1         # 回调Javascript方法 例如：faker.Window_get_frames


class FlagImmutable:
    instance = 1 << 0
    prototype = 1 << 1


class V8Attribute:
    kNone = 0
    ReadOnly = 1 << 0  # ReadOnly, i.e., not writable
    DontEnum = 1 << 1  # DontEnum, i.e., not enumerable.
    DontDelete = 1 << 2  # DontDelete, i.e., not configurable


class FlagLocation:
    kInstance = 0
    kPrototype = 1
    kInterface = 2


class FlagReceiverCheck:
    kCheck = 0
    kDoNotCheck = 1


class FlagCrossOriginCheck:
    kCheck = 0
    kDoNotCheck = 1


class FlagExposed:
    kNo = 0
    kYes = 1


# 控制js object对象是否能使用 "new Test()" 和 "Test()"语法
class FlagConstructor:
    kDontAll = 0
    kNew = 1 << 0
    kCall = 1 << 1
    kAll = kNew | kCall


class SideEffectType:
    kHasSideEffect = 0
    kHasNoSideEffect = 1
    kHasSideEffectToReceiver = 2


class FlagArrayProto:
    iterator = 1 << 0
    entries = 1 << 1
    keys = 1 << 2
    values = 1 << 3
    forEach = 1 << 4
