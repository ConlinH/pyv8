#!/usr/bin/env python
"""
运行pyv8测试的脚本
支持unittest和pytest两种方式
"""
import unittest
import sys
import os
import argparse

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_unittest():
    """使用unittest运行所有测试"""
    # 导入所有测试模块
    from tests.test_context import TestContext
    from tests.test_script import TestScript
    from tests.test_jsobject import TestJSObject
    from tests.test_jsfunction import TestJSFunction
    from tests.test_jspromise import TestJSPromise
    from tests.test_jstypedarray import TestJSTypedArray
    from tests.test_pyclass import TestPyClass
    from tests.test_exception import TestException
    from tests.test_conversion import TestConversion
    from tests.test_faker import TestFaker
    from tests.test_multiple_context import TestMultipleContext

    # 创建测试套件
    test_suite = unittest.TestSuite()

    # 添加测试类
    test_classes = [
        TestContext,
        TestScript,
        TestJSObject,
        TestJSFunction,
        TestJSPromise,
        TestJSTypedArray,
        TestPyClass,
        TestException,
        TestConversion,
        TestFaker,
        TestMultipleContext
    ]

    for test_class in test_classes:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result.wasSuccessful()

def run_pytest():
    """使用pytest运行所有测试"""
    try:
        import pytest
    except ImportError:
        print("pytest未安装，使用pip install pytest安装中...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest" ])
        import pytest

    # 运行pytest
    return pytest.main(["-v", "tests"]) == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="运行pyv8测试")
    parser.add_argument("--pytest", action="store_true", help="使用pytest运行测试")
    args = parser.parse_args()

    if args.pytest:
        success = run_pytest()
    else:
        success = run_unittest()

    sys.exit(0 if success else 1)
