import unittest
import pyv8
from pyv8.tools import ConstructorConfig, exposed_constructs
from pyv8.flag import *

class TestFaker(unittest.TestCase):
    """测试faker模块的功能"""
    
    def setUp(self):
        """每个测试前创建一个新的上下文"""

        @ConstructorConfig(exposed=FlagExposed.kYes, constructor=FlagConstructor.kDontAll, length=0, v8_array=0, immutable=FlagImmutable.instance | FlagImmutable.prototype, has_constructor=1)
        class Window: 
            # 只为有__v8_global_this__标记的全局对象设置faker对象
            __v8_global_this__ = True 

            def __v8_name_get__(self, name):
                if name in exposed_constructs:
                    return exposed_constructs[name]


        self.context = pyv8.Context(Window(), hook=True)
    
    def tearDown(self):
        """测试结束后清理上下文"""
        del self.context
    
    def test_faker(self):
        """测试faker对象的是否被创建"""
        faker = self.context.exec_js("globalThis.faker;")
        self.assertIsInstance(faker, pyv8.JSObject)

    def test_v8_version(self):
        """测试window对象"""
        v8_version = self.context.exec_js("faker.v8_version")
        self.assertEqual(v8_version, '12.5.99')
        
    def test_print(self):
        """测试print函数"""
        self.context.exec_js("faker.print('Hello, World!')")
        
        # 测试print函数不会调用对象的toString方法
        self.context.exec_js("a = {i:0, toString: function toString(){this.i+=1; return 'a'}}; faker.print(a, a);")
        self.assertEqual(self.context.exec_js("a.i"), 0)

    def test_native_wrapper(self):
        """测试native_wrapper函数"""
        result = self.context.exec_js("""
            fn =faker.native_wrapper({
                name: "test", 
                length: 0, 
                cb: function () {
                    return "this is native wrapper function";
                }
            });
            fn.toString();
        """)
        self.assertEqual(result, "function test() { [native code] }")

    def test_hook(self):
        """测试hook对象的属性访问"""
        self.context.exec_js("faker.hook=true;")
        self.context.exec_js("a=1;")
        self.context.exec_js("Window")

if __name__ == "__main__":
    unittest.main()
