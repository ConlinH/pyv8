# pyv8

pyv8是一个强大的Python扩展，提供了Python与Google V8 JavaScript引擎之间的桥梁。它允许您在Python中执行JavaScript代码，并实现Python与JavaScript之间的无缝交互。

pyv8主要是为了js逆向时补环境提供更多底层支持，为一比一模拟chromium内置原型对象提供基础api。

## 特性

- 在Python中执行JavaScript代码
- 将Python对象暴露给JavaScript环境
- 访问和操作JavaScript对象
- 支持JavaScript Promise
- 支持JavaScript TypedArray
- 内置调试工具（DevTools）
- 支持JavaScript异常处理

## 安装

### 系统要求

- Python 3.10 或更高版本
- 支持的平台：Windows, Linux


### 通过pip安装

```bash
pip install git+https://github.com/ConlinH/pyv8
```

### 从源码构建

1. 克隆仓库：

```bash
git clone https://github.com/ConlinH/pyv8.git
cd pyv8
```

2. 使用pyproject.toml构建和安装（推荐）：

```bash
# 开发模式安装
pip install -e .

# 或者直接安装
pip install .
```

3. 检测是否安装成功
```bash
python -c "from pyv8 import _pyv8; print(_pyv8.v8_version())"
```

4.卸载：

```bash
pip uninstall pyv8
```

## 开发与测试

### 使用tox进行测试

项目使用tox进行自动化测试，支持多个Python版本：

```bash
# 安装tox
pip install tox

# 运行所有测试环境
tox

```

## 快速入门

### 基本用法

```python
import pyv8

class Window: pass

# 创建一个JavaScript执行上下文
context = pyv8.Context(Window)

# 执行JavaScript代码
result = context.exec_js("1 + 2")
print(result)  # 输出: 3

# 执行更复杂的JavaScript代码
result = context.exec_js("""
    function add(a, b) {
        return a + b;
    }
    add(5, 7);
""")
print(result)  # 输出: 12
```

### 将Python函数暴露给JavaScript

```python
import pyv8

class Window: pass

def hello(name):
    return f"Hello, {name} from Python!"

context = pyv8.Context(Window())
context.expose(hello)

result = context.exec_js("hello('World')")
print(result)  # 输出: Hello, World from Python!
```

### 使用DevTools调试

```python
import pyv8
from pyv8 import start_devtools

class Window:
    __v8_global_this__ = True


# 执行JavaScript代码
def callback(ctx):
    ctx.exec_js("""
        function test() {
            console.log('Testing DevTools');
            debugger;  // 这将在DevTools中触发断点
            return 'Done';
        }
        test();
    """)

context = pyv8.Context(Window())
# 启动DevTools调试服务器
start_devtools(context, callback=callback, port=9005)

# 控制台会输出DevTools URL，可以在Chrome浏览器中打开进行调试
```

## 高级用法

查看测试用例


## 致谢

- [Google V8 Engine](https://v8.dev/)

## 联系方式

- 作者：conlin
- 邮箱：995018884@qq.com
- GitHub：[https://github.com/ConlinH/pyv8](https://github.com/ConlinH/pyv8)
