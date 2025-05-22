import unittest
import pyv8

class TestConversion(unittest.TestCase):
    """测试Python和JavaScript类型之间的转换"""
    
    def setUp(self):
        """每个测试前创建一个新的上下文"""
        class Window: pass
        self.context = pyv8.Context(Window())
    
    def tearDown(self):
        """测试结束后清理上下文"""
        del self.context
    
    def test_number_conversion(self):
        """测试数字类型转换"""
        # Python -> JavaScript
        self.context.expose(py_int=42, py_float=3.14)
        result = self.context.exec_js("py_int + py_float")
        self.assertAlmostEqual(result, 45.14)
        
        # JavaScript -> Python
        js_int = self.context.exec_js("42")
        js_float = self.context.exec_js("3.14")
        self.assertEqual(js_int, 42)
        self.assertAlmostEqual(js_float, 3.14)
    
    def test_string_conversion(self):
        """测试字符串类型转换"""
        # Python -> JavaScript
        self.context.expose(py_str="Hello, World!")
        result = self.context.exec_js("py_str + '!'")
        self.assertEqual(result, "Hello, World!!")
        
        # JavaScript -> Python
        js_str = self.context.exec_js("'Hello, World!'")
        self.assertEqual(js_str, "Hello, World!")
        
        # Unicode字符
        unicode_str = "你好，世界！"
        self.context.expose(py_unicode=unicode_str)
        result = self.context.exec_js("py_unicode")
        self.assertEqual(result, unicode_str)
    
    def test_boolean_conversion(self):
        """测试布尔类型转换"""
        # Python -> JavaScript
        self.context.expose(py_true=True, py_false=False)
        result1 = self.context.exec_js("py_true === true")
        result2 = self.context.exec_js("py_false === false")
        self.assertTrue(result1)
        self.assertTrue(result2)
        
        # JavaScript -> Python
        js_true = self.context.exec_js("true")
        js_false = self.context.exec_js("false")
        self.assertEqual(js_true, True)
        self.assertEqual(js_false, False)
    
    def test_none_null_undefined_conversion(self):
        """测试None/null/undefined类型转换"""
        # Python -> JavaScript
        self.context.expose(py_none=None)
        result1 = self.context.exec_js("py_none === undefined")
        self.assertTrue(result1)
        
        # JavaScript -> Python
        js_null = self.context.exec_js("null")
        js_undefined = self.context.exec_js("undefined")
        self.assertEqual(js_null, pyv8.Null)
        self.assertEqual(js_undefined, pyv8.Undefined)
    
    def test_list_array_conversion(self):
        """测试列表/数组类型转换"""
        # Python -> JavaScript
        py_list = [1, 2, 3, "four", True]
        self.context.py_list = py_list

        # 验证数组长度
        length = self.context.exec_js("py_list.length")
        self.assertEqual(length, 5)
        
        # 验证数组元素
        result0 = self.context.exec_js("py_list[0]")
        result3 = self.context.exec_js("py_list[3]")
        result4 = self.context.exec_js("py_list[4]")
        self.assertEqual(result0, 1)
        self.assertEqual(result3, "four")
        self.assertEqual(result4, True)
        
        # JavaScript -> Python
        js_array = self.context.exec_js("[1, 2, 3, 'four', true]")
        self.assertEqual(list(js_array), [1, 2, 3, "four", True])
    
    def test_dict_object_conversion(self):
        """测试字典/对象类型转换"""
        # Python -> JavaScript
        py_dict = {"a": 1, "b": "two", "c": True}
        self.context.py_dict=py_dict
        
        # 验证对象属性
        result_a = self.context.exec_js("py_dict.a")
        result_b = self.context.exec_js("py_dict.b")
        result_c = self.context.exec_js("py_dict.c")
        self.assertEqual(result_a, 1)
        self.assertEqual(result_b, "two")
        self.assertEqual(result_c, True)
        
        # JavaScript -> Python
        js_object = self.context.exec_js("({a: 1, b: 'two', c: true})")
        self.assertEqual(js_object["a"], 1)
        self.assertEqual(js_object["b"], "two")
        self.assertEqual(js_object["c"], True)
    
    def test_nested_structure_conversion(self):
        """测试嵌套结构类型转换"""
        # Python -> JavaScript
        py_nested = {
            "array": [1, 2, 3],
            "object": {"a": 1, "b": 2},
            "mixed": [{"x": 1}, [2, 3], 4]
        }
        self.context.py_nested=py_nested
        
        # 验证嵌套结构
        array_length = self.context.exec_js("py_nested.array.length")
        object_a = self.context.exec_js("py_nested.object.a")
        mixed_0_x = self.context.exec_js("py_nested.mixed[0].x")
        mixed_1_1 = self.context.exec_js("py_nested.mixed[1][1]")
        
        self.assertEqual(array_length, 3)
        self.assertEqual(object_a, 1)
        self.assertEqual(mixed_0_x, 1)
        self.assertEqual(mixed_1_1, 3)
        
        # JavaScript -> Python
        js_nested = self.context.exec_js("""
            ({
                array: [1, 2, 3],
                object: {a: 1, b: 2},
                mixed: [{x: 1}, [2, 3], 4]
            })
        """)
        
        self.assertEqual(list(js_nested["array"]), [1, 2, 3])
        self.assertEqual(js_nested["object"]["a"], 1)
        self.assertEqual(js_nested["mixed"][0]["x"], 1)
        self.assertEqual(list(js_nested["mixed"][1]), [2, 3])
        self.assertEqual(js_nested["mixed"][2], 4)
    
    def test_function_conversion(self):
        """测试函数类型转换"""
        # Python -> JavaScript
        def py_func(a, b):
            return a + b
        
        self.context.expose(py_func=py_func)
        result = self.context.exec_js("py_func(5, 3)")
        self.assertEqual(result, 8)
        
        # JavaScript -> Python
        js_func = self.context.exec_js("function test (a, b) { return a * b; }; test;")
        result = js_func(5, 3)
        self.assertEqual(result, 15)
    
    def test_date_conversion(self):
        """测试日期类型转换"""
        # JavaScript -> Python
        js_date = self.context.exec_js("new Date('2023-01-01T00:00:00Z')")
        
        # 验证日期对象
        self.assertIsInstance(js_date, pyv8.JSObject)
        
        # 获取日期的年份
        year = js_date.getUTCFullYear()
        self.assertEqual(year, 2023)
    
    def test_regexp_conversion(self):
        """测试正则表达式类型转换"""
        # JavaScript -> Python
        js_regexp = self.context.exec_js("/^hello/i")
        
        # 验证正则表达式对象
        self.assertIsInstance(js_regexp, pyv8.JSObject)
        
        # 测试正则表达式匹配
        test_result = self.context.exec_js("(function(re) { return re.test('Hello World'); })")(js_regexp)
        self.assertTrue(test_result)

if __name__ == "__main__":
    unittest.main()
