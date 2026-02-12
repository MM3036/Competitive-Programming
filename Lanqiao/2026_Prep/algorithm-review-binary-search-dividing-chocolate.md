# 📝 算法复盘笔记：二分答案基础（以《分巧克力》为例）

## 1. 题目描述 (Problem Description)

- **题目来源**：蓝桥杯 2017 年省赛 B 组
- **题目名称**：分巧克力

### 情境描述
有 $N$ 块长方形的巧克力，每块巧克力的长和宽分别为 $H_i$ 和 $W_i$。现在需要从这 $N$ 块巧克力中切出 $K$ 块形状、大小完全相同的正方形巧克力分给 $K$ 位小朋友。

### 具体要求
1.  **形状限制**：切出的巧克力必须是正方形，边长设为 $X$。
2.  **数量限制**：切出的正方形总数至少为 $K$ 块（允许超过 $K$ 块）。
3.  **目标**：在满足上述条件的前提下，使正方形的边长 $X$ 尽可能大。

### 输入格式
- 第一行包含两个整数 $N, K$ ($1 \le N, K \le 100,000$)。
- 接下来 $N$ 行，每行包含两个整数 $H_i, W_i$ ($1 \le H_i, W_i \le 100,000$)。

### 输出格式
- 输出切出的正方形巧克力最大可能的边长。

---

## 2. 核心知识点 (Key Concepts)

本题考察的是 **“二分答案” (Binary Search on Answer)** 算法，具体属于 **“最大化可行解”** 类问题。

### A. 算法选择依据
1.  **单调性 (Monotonicity)**：答案 $X$ 具有明显的单调性。
    - 若边长 $X$ 可行（能切出 $\ge K$ 块），则所有 $X' < X$ 的边长一定也可行。
    - 若边长 $X$ 不可行（切不出 $K$ 块），则所有 $X' > X$ 的边长一定也不可行。
2.  **解空间确定**：答案 $X$ 的取值范围在 $[1, 100000]$ 之间，且为整数。
3.  **验证简单**：验证一个给定的 $X$ 是否可行（Check 函数）的时间复杂度为 $O(N)$，远低于直接求解。

### B. 二分模版应用 (Template Type)
本题要求最大的满足条件的值，即在数轴上寻找**可行区间的右边界**。

- **区间更新逻辑**：
    - 若 `check(mid)` 为真（可行）：答案可能是 `mid` 或更大，故区间变为 `[mid, r]`，即 `l = mid`。
    - 若 `check(mid)` 为假（不可行）：答案一定小于 `mid`，故区间变为 `[l, mid - 1]`，即 `r = mid - 1`。
- **防死循环处理**：
    - 由于使用了 `l = mid`，计算中点时必须向上取整，即 `mid = (l + r + 1) // 2`。

### C. 贪心判定逻辑 (Check Function)
对于任意一块 $H \times W$ 的矩形，能切出的边长为 $x$ 的正方形数量计算公式为：

$$
\text{Count} = \lfloor \frac{H}{x} \rfloor \times \lfloor \frac{W}{x} \rfloor
$$

总数量为所有矩形切出数量之和。若总和 $\ge K$，则返回 `True`。

---

## 3. 实战失误分析 (Error Analysis)

在代码实现过程中，算法逻辑与二分模版均正确，但在数学运算的**运算符优先级**上出现了严重失误。

### A. 失误详情

**错误代码**：
```python
num += temp[i][0] // mid * temp[i][1] // mid
```

**执行顺序分析**：
Python 中整除 `//` 与乘法 `*` 优先级相同，且结合性为**从左到右**。上述代码实际上等价于：
```python
((H // mid) * W) // mid
```

**后果**：
先计算了“长能切几段”，然后乘以了“宽”，最后再除以“边长”。这导致计算出的块数远大于实际能切出的块数，使得 `check` 函数误判为 `True`，最终求出的 $X$ 偏大。

### B. 修正方案

**修正代码**：
```python
num += (temp[i][0] // mid) * (temp[i][1] // mid)
```

**原理**：
利用括号强制规定运算顺序，先分别计算长和宽各能切出多少段，再将两者的段数相乘，得到该块巧克力的总切分数。

---

## 4. 复杂度评估 (Complexity)

- **时间复杂度**：$O(N \log L)$
    - 其中 $N$ 为巧克力数量，$L$ 为边长最大值（$10^5$）。
    - 二分查找循环次数为 $\log_2(100000) \approx 17$ 次。
    - 每次 Check 函数遍历 $N$ 个元素。
- **空间复杂度**：$O(N)$
    - 用于存储 $N$ 个矩形的长宽数据。

---

## 5. 正确代码 (Correct Solution)

```python
import sys

# 1. 高效读取输入
# 使用 iterator 避免切片产生的内存开销，适合大数据量读取
def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    N = int(next(iterator))
    K = int(next(iterator))
    
    chocolates = []
    max_len = 0
    for _ in range(N):
        h = int(next(iterator))
        w = int(next(iterator))
        chocolates.append((h, w))
        # 记录最大边长，用于设定二分右边界（虽然题目说10万，但动态获取更稳健）
        max_len = max(max_len, h, w)

    # 2. 核心 Check 函数
    def check(mid):
        if mid == 0: return False # 防止除以0（虽然后面 l 从 1 开始，防御性编程）
        
        count = 0
        # 优化点：直接解包 (Unpacking)，比 temp[i][0] 快且清晰
        for h, w in chocolates:
            # 修正点：必须加括号！先算长宽各切几段，再相乘
            count += (h // mid) * (w // mid)
            
            # 剪枝优化：一旦数量够了立即停止，无需算完剩下的
            if count >= K:
                return True
        return False

    # 3. 二分答案（模版 1：求最大值）
    l, r = 1, max_len # 右边界设为数据中的最大边长
    
    while l < r:
        # 重点：因为下面是 l = mid，这里必须 +1 (向上取整) 避免死循环
        mid = (l + r + 1) // 2
        
        if check(mid):
            l = mid      # mid 可行，尝试更大的
        else:
            r = mid - 1  # mid 不可行，太大了
            
    print(l)

if __name__ == '__main__':
    solve()

```
