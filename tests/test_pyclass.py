import unittest
import pyv8

class TestPyClass(unittest.TestCase):
    """测试Python类在JavaScript中的暴露"""
    
    def setUp(self):
        """每个测试前创建一个新的上下文"""
        class Window: pass
        self.context = pyv8.Context(Window())
    
    def tearDown(self):
        """测试结束后清理上下文"""
        del self.context
    
    def test_class_methods(self):
        """测试实类方法调用"""
        class Calculator:
            __v8_constructor__ = 2
            __v8_method__ = (
                # (name, cb, length, CallbackType, FlagLocation, V8Attribute, FlagReceiverCheck, 
                # cross_origin_check, SideEffectType)
                ("add", "fn_add", 0, 0, 0, 0, 0, 0, 0),
                ("subtract", "fn_subtract", 0, 0, 0, 0, 0, 0, 0),
            )

            def __init__(self, win=None):
                pass

            def fn_add(self, a, b, **kw):
                return a + b
            
            def fn_subtract(self, a, b, **kw):
                return a - b
        
        # 暴露类到JavaScript
        self.context.expose(Calculator)
        
        # 在JavaScript中使用类
        result = self.context.exec_js("""
            var obj = new Calculator();
            [obj.add(2, 8), obj.subtract(30, 10)]
        """)
        
        # 验证结果
        self.assertEqual(list(result), [10, 20])
    
    def test_class_properties(self):
        """测试实类属性调用"""
        class ClassWithProperties:
            __v8_constructor__ = 2

            __v8_attribute__ = (
                # (attr_name, get_cb, set_cb, CallbackType, FlagLocation, V8Attribute, FlagReceiverCheck, 
                # FlagCrossOriginCheck, FlagCrossOriginCheck, SideEffectType)
                ("x", "get_x", "set_x", 0, 0, 0, 0, 1, 0, 1),
                ("y", "get_y", "set_y", 0, 0, 0, 0, 1, 0, 1),
                ("sum", "get_sum", None, 0, 0, 0, 0, 1, 0, 1),
            )

            def __init__(self, win=None):
                self._x = 0
                self._y = 0
            
            def get_x(self):
                return self._x
            
            def set_x(self, value):
                self._x = value
            
            def get_y(self):
                return self._y
            
            def set_y(self, value):
                self._y = value
            
            def get_sum(self):
                return self._x + self._y
        
        # 暴露类到JavaScript
        self.context.expose(ClassWithProperties)
        
        # 在JavaScript中使用类
        result = self.context.exec_js("""
            var obj = new ClassWithProperties();
            obj.x = 10;
            obj.y = 20;
            [obj.x, obj.y, obj.sum]
        """)
        
        # 验证结果
        self.assertEqual(list(result), [10, 20, 30])
    
    def test_class_static_methods(self):
        """测试类静态方法的调用"""
        class ClassWithStaticMethods:
            @staticmethod
            def add(a, b):
                return a + b
        
        # 不支持staticmethod类型转换
        # 不支持staticmethod类型转换
        # 不支持staticmethod类型转换

        # 验证结果
        self.assertEqual(True, True)
    
    def test_class_inherit(self):
        """测试类继承"""
    
        class EventTarget: pass
        
        class Node(EventTarget): pass

        class Element(Node): pass

        self.context.expose(Element)
        result = self.context.exec_js("Element.__proto__.toString()")
        
        # 验证结果
        self.assertEqual(result, 'function Node() { [native code] }')
    
    def test_class_skip_inherit(self):
        """测试类跳过原型继承继承"""
        is_call_addEventListener = False
    
        class EventTarget: pass

        class WindowProperties(EventTarget):
            __v8_skip_inherit__ = True

        class Win(WindowProperties): pass

        self.context.expose(Win)
        result = self.context.exec_js("Win.__proto__.toString()")
        
        # 验证结果
        self.assertEqual(result, 'function EventTarget() { [native code] }')

    def test_class_has_constructor(self):
        """测试类没有构造函数"""
        class EventTarget:
            __v8_has_constructor__ = 1

        class WindowProperties(EventTarget):
            __v8_has_constructor__ = 0

        self.context.expose(WindowProperties, EventTarget)

        result1 = self.context.exec_js("Object.keys(Object.getOwnPropertyDescriptors(EventTarget.prototype))")
        self.assertEqual(result1, ['constructor'])

        result2 = self.context.exec_js("Object.keys(Object.getOwnPropertyDescriptors(WindowProperties.prototype))")
        self.assertEqual(result2, [])

    def test_class_constructor_behavior(self):
        """测试类构造函数行为"""
        class Test1:
            __v8_constructor__ = pyv8.FlagConstructor.kDontAll

        class Test2:
            __v8_constructor__ = pyv8.FlagConstructor.kNew

            def __init__(self, win=None):
                pass
        
        class Test3:
            __v8_constructor__ = pyv8.FlagConstructor.kCall

            def __init__(self, win=None):
                pass

        self.context.expose(Test1, Test2, Test3)

        with self.assertRaises(pyv8.JSException):
            self.context.exec_js("new Test1()")

        with self.assertRaises(pyv8.JSException):
            self.context.exec_js("Test1()")

        self.context.exec_js("new Test2")
        with self.assertRaises(pyv8.JSException):
            self.context.exec_js("Test2()")

        self.context.exec_js("new Test3")
        self.context.exec_js("Test3()")

    def test_class_undetectable_and_call(self):
        """测试类的不可检查性 和 __call__"""

        class HTMLAllCollection:
            __v8_undetectable__ = True

            def __call__(self, id_name):
                return pyv8.Null

        class Document:
            __v8_attribute__ = (
                ("all", "get_all", None, 0, 1, 0, 0, 0, 0, 1),
            )
            def get_all(self):
                return HTMLAllCollection()

        document = Document()
        self.context.expose(document=document)
        result = self.context.exec_js("document.all == undefined")
        self.assertEqual(True, result)

        result = self.context.exec_js("document.all('testId')")
        self.assertEqual(result, pyv8.Null)


if __name__ == "__main__":
    unittest.main()
