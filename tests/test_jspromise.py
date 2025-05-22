import unittest
import pyv8
import time

class TestJSPromise(unittest.TestCase):
    """测试JavaScript Promise的使用"""
    
    def setUp(self):
        """每个测试前创建一个新的上下文"""
        class Window: pass
        self.context = pyv8.Context(Window())
    
    def tearDown(self):
        """测试结束后清理上下文"""
        del self.context
    
    def test_is_promise(self):
        """测试Promise转换"""
        promise = self.context.exec_js("""
            new Promise((resolve, reject) => {
                resolve('success');
            });
        """)
        self.assertIsInstance(promise, pyv8.JSPromise)
    
    def test_promise_then(self):
        """测试Promise then"""
        def callback(ret):
            self.assertEqual(ret, 'success')
        
        promise = self.context.exec_js("""
            new Promise((resolve, reject) => {
                resolve('success');
            });
        """)
        promise.then(callback)

if __name__ == "__main__":
    unittest.main()
