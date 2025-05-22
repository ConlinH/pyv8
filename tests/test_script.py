import unittest
import pyv8

class TestScript(unittest.TestCase):
    """测试JavaScript脚本的编译和执行"""
    
    def setUp(self):
        """每个测试前创建一个新的上下文"""
        class Window: pass
        self.context = pyv8.Context(Window())
    
    def tearDown(self):
        """测试结束后清理上下文"""
        del self.context
    
    def test_script_creation(self):
        """测试脚本创建"""
        script = pyv8.Script(self.context, "1 + 1")
        self.assertIsInstance(script, pyv8.Script)
    
    def test_script_execution(self):
        """测试脚本执行"""
        script = pyv8.Script(self.context, "1 + 1")
        result = self.context.exec_js(script)
        self.assertEqual(result, 2)
    
    def test_script_with_filename(self):
        """测试带有文件名的脚本"""
        script = pyv8.Script(self.context, "(new Error).stack", "https://www.xxx.com/test.js")
        result = self.context.exec_js(script)
        self.assertIn("https://www.xxx.com/test.js", result)
        #self.assertEqual(result, 2)

if __name__ == "__main__":
    unittest.main()
