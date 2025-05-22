import unittest
import pyv8

class TestException(unittest.TestCase):
    """测试JavaScript异常处理"""
    
    def setUp(self):
        """每个测试前创建一个新的上下文"""
        class Window: pass
        self.context = pyv8.Context(Window())
    
    def tearDown(self):
        """测试结束后清理上下文"""
        del self.context
    
    def test_catch_exception(self):
        """测试JavaScript语法错误"""
        with self.assertRaises(pyv8.JSException):
            self.context.exec_js("1 + ")
        
        with self.assertRaises(pyv8.JSException):
            self.context.exec_js("throw new Error('Test error')")
        
    def test_throw_exception(self):
        """测试Python抛出异常到JavaScript"""
        class V8Error(Exception):
            
            # 标记为V8的Error异常
            __v8_error__ = True 
            
        def raise_exception():
            raise V8Error("Test exception")
            
        self.context.expose(raise_exception=raise_exception)
        
        result = self.context.exec_js("""
                var ret;
                try{
                    raise_exception();
                } catch(e) {
                    ret = {message: e.message, name: e.name, stack: e.stack} 
                };
                ret
            """)
        self.assertEqual(result["message"], "Test exception")
        self.assertEqual(result["name"], "Error")
        self.assertIn("Error: Test exception\n    at <anonymous>", result["stack"])

if __name__ == "__main__":
    unittest.main()
