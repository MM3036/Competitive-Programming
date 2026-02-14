# 算法笔记：实数二分与 Python 输出技巧

## 一、 题目回顾：一元三次方程求解 (蓝桥杯/NOIP真题)

### 1. 题目描述
有形如 $ax^3 + bx^2 + cx + d = 0$ 的一元三次方程。 给定各项系数 $a, b, c, d$（均为实数），已知该方程存在三个不同实根，且根与根之差的绝对值 $\ge 1$。 要求由小到大依次输出这三个实根。

### 2. 输入输出格式
- **输入：** 一行，4 个实数 $a, b, c, d$。
- **输出：** 一行，3 个实数，精确到小数点后 2 位，中间用空格隔开。
- **数据范围：** $|a|,|b|,|c|,|d| \le 10$，根的范围在 $[-100, 100]$ 之间。

---

## 二、 核心算法知识点

### 1. 实数二分 (Real Number Binary Search)
与整数二分不同，实数二分处理连续区间，不需要处理边界的 `+1` 或 `-1` 问题。

- **区间更新：** 仅使用 `l = mid` 或 `r = mid`。
- **终止条件：**
  1.  **精度控制法：** `while r - l > 1e-7:` (精度需比题目要求高 2-3 个数量级)。
  2.  **固定循环次数法（推荐）：** `for _ in range(100):` (循环 100 次可达到 $2^{-100}$ 精度，绝对安全且无死循环风险)。

### 2. 零点存在性定理
- 如果函数 $f(x)$ 在区间 $[l, r]$ 上连续，且 $f(l) \cdot f(r) < 0$（端点异号），则该区间内至少存在一个根。
- **解题策略：** 结合题目给出的“根间距 $\ge 1$”条件，枚举所有长度为 1 的子区间 $[i, i+1]$，若端点异号则进行二分查找。

---

## 三、 调试记录与常见误区

在编写实数二分代码时，需注意以下易错点：

### 1. 除法运算符错误
- ❌ **错误：** `mid = (l + r) // 2` (`//` 为整除，会导致死循环或精度丢失)。
- ✅ **正确：** `mid = (l + r) / 2` (实数除法)。

### 2. 输入方式选择
- **问题：** 本地调试（如 PyCharm）中使用 `sys.stdin.read()` 可能会导致程序挂起等待 EOF 信号。
- **解决：** 对于单行简单输入，优先使用 `input()`；大数据量（$10^5$ 行以上）再考虑 `sys.stdin`。

### 3. 函数与变量作用域
- **优化：** 系数 $a,b,c,d$ 应在主程序读取一次，设为全局变量，避免在 Check 函数内部重复读取。
- **拼写：** 保持函数定义与调用名一致（如 `func` vs `fun`）。

---

## 四、 Python 高阶技巧：列表推导式与 f-string

利用 Python 的 `f-string` 结合列表推导式，可以高效处理复杂的输出格式。

### 万能公式
```python
print("分隔符".join(f"{变量:格式}" for 变量 in 列表))
```

### 典型应用场景

#### 1. 百分比输出 (概率/统计)
自动乘以 100 并添加 `%` 符号。
```python
probs = [0.12345, 0.5, 1.0]
print(" ".join(f"{x:.1%}" for x in probs))
# 输出：12.3% 50.0% 100.0%
```

#### 2. 整数补零 (编号/时间)
指定位宽，不足位左侧补 0。
```python
nums = [5, 12, 123]
print(" ".join(f"{x:03d}" for x in nums))
# 输出：005 012 123
```

#### 3. 进制转换 (位运算/计算机基础)
快速转换为十六进制（`x`/`X`）或二进制（`b`）。
```python
vals = [10, 255, 15]
print(" ".join(f"0x{x:02X}" for x in vals))
# 输出：0x0A 0xFF 0x0F
```

#### 4. 坐标点格式化 (几何)
直接解包元组并嵌入格式中。
```python
points = [(1, 2), (3, 4)]
print(", ".join(f"({x},{y})" for x, y in points))
# 输出：(1,2), (3,4)
```

#### 5. 带条件过滤输出
在推导式中加入 `if` 筛选数据。
```python
data = [-5, 3, 10]
# 仅保留正数并保留两位小数
print(" ".join(f"{x:.2f}" for x in data if x > 0))
# 输出：3.00 10.00
```

---

## 五、 正确代码参考

```python
import sys

# 1. 兼容性写法：如果在本地测试，input() 更方便；在 OJ 上这也完全没问题
try:
    line = sys.stdin.readline() 
    if not line: # 处理空输入情况
        line = input()
    a, b, c, d = map(float, line.split())
except ValueError:
    # 这是一个保护，防止没有输入时报错
    a, b, c, d = 0, 0, 0, 0

def func(x):
    return a * (x ** 3) + b * (x ** 2) + c * x + d

def bi_find(l, r):
    # 记录左端点的符号
    start_sign = 1 if func(l) > 0 else -1
    
    # 二分 100 次
    for i in range(100):
        mid = (l + r) / 2
        mid_val = func(mid)
        
        if mid_val == 0:
            return mid
            
        # 符号判断：如果 mid 和 左边同号，说明根在右边
        if (1 if mid_val > 0 else -1) == start_sign:
            l = mid
        else:
            r = mid
    return l

result = []

# 遍历 [-100, 100)
for i in range(-100, 100):
    l, r = i, i + 1
    # 2. 修正这里的拼写错误：fun -> func
    fl = func(l)
    fr = func(r)
    
    # 这种情况是左端点恰好是根
    if abs(fl) < 1e-9: # 用 abs < 极小值 替代 == 0 更安全
        result.append(l)
        continue
    
    # 异号说明中间有根
    if fl * fr < 0:
        result.append(bi_find(l, r))

# 3. 补漏：检查最右边的端点 100 是否是根
if abs(func(100)) < 1e-9:
    result.append(100)

print(" ".join(f"{x:.2f}" for x in result))
```
```

---
