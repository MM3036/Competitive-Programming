# 方法论：从模拟到数学建模的思维跃迁

> **💡 核心要义：贡献法的核心是思想转变 —— 不再枚举结果，而是分析产生结果的原因。**

## 题目描述
你需要构造两个矩形，矩形 A 和矩形 B。

### 变量定义
*   矩形的边长 $W_A, H_A, W_B, H_B$ 均为正整数。
*   **限制**：两个矩形的面积之积不得超过 $L$。即：$(W_A \cdot H_A) \cdot (W_B \cdot H_B) \le L$。
*   **能量定义**：矩形的“能量”为它的半周长（即 $W + H$）。

### 目标
计算在所有满足条件的方案中，（矩形 A 的能量 $\times$ 矩形 B 的能量）的总和。

---

## 1. 核心思维转变 (Core Paradigm Shift)

解决数论约束问题最关键的觉醒，是从 **模拟思维 (局部视角)** 转向 **贡献思维 (全局视角)**。

### ❌ 模拟法的陷阱 (The Simulation Trap)

* **心智模型：** 站在具体的数字 $N$ 上，试图向下“挖掘”它的属性（例如：去算 12 的约数有哪些）。
* **思维缺陷：** “站在每一个具体的数字上往下挖，会把自己绕进无限的细节里。”
* **复杂度后果：** 通常会导致 $O(N\sqrt{N})$ 或 $O(N^2)$ 的复杂度，直接导致 TLE (超时)。
* **我的错误：** 试图在循环里单独对每个数字进行计算。

### ✅ 贡献法的破局 (The Contribution Technique)

* **心智模型：** “对整个数轴进行地毯式轰炸。”
* **核心洞察：** 不要问“12 的约数是谁？”，要问 **“2 是谁的约数？”**
* **关键动作：** 枚举 **因子 (原子)**，然后将其贡献分发给它所有的 **倍数**。
* **关于“能量”的顿悟：**
    > "我不需要去硬算 $L$ 的约数。通过遍历因子，一遍遍历就把所有约数找到，**不光找到还把能量算出来**。"

---

## 2. 解题三板斧 (The "Three-Step Combo")

针对 $A \cdot B \le L$ 或 $A + B \le L$ 这类约束问题，遵循以下严格的流水线：

### 第一步：数学建模 (Mathematical Modeling)

**铁律：** 公式没写出来之前，绝不碰键盘。

* 清晰定义变量（如 $u, v$）。
* 推导求和公式。
    * 例如：$$Ans = \sum_{u=1}^{L} (E[u] \times \sum_{v=1}^{Limit} E[v])$$
* 识别 **变量联动性 (Linkage)**：
    * $A + B \le L \Rightarrow$ 倒三角区域 (强相关，需特殊处理)。
    * $A, B \le L \Rightarrow$ 矩形区域 (独立，可直接乘)。

### 第二步：调和级数筛 (Harmonic Sieve)

**目标：** 高效预处理 $[1, L]$ 范围内所有数字的属性（约数、和等）。
**复杂度：** $O(L \log L)$。

```python
# 模板：分发贡献
properties = [0] * (L + 1)

# 外层枚举因子
for factor in range(1, L + 1):
    # 内层枚举倍数
    for multiple in range(factor, L + 1, factor):
        # 更新倍数的属性
        properties[multiple] += calculation(factor) 
```

### 第三步：前缀和优化 (Prefix Sum Optimization)

**目标：** 将最终统计时的内层循环从 $O(N)$ 降维到 $O(1)$。
**应用场景：** 当 $v$ 的取值范围依赖于 $u$ 时（例如 $v \le L/u$）。

```python
# 模板：O(1) 区间查询
prefix_sum = [0] * (L + 1)
for i in range(1, L + 1):
    prefix_sum[i] = prefix_sum[i-1] + properties[i]

# 最终统计
ans = 0
for u in range(1, L + 1):
    max_v = L // u  # 联动限制
    ans += properties[u] * prefix_sum[max_v]
```

---

## 3. 错题集与教训 (Critical Mistakes & Lessons)

### 💀 错误一：“对称性”陷阱

* **场景：** 题目给定 $A + B \le L$。
* **我的操作：** 只算了一半的范围，然后简单粗暴地乘以 4，误以为是矩形分布。
* **修正：** 合法区域是一个 **倒三角形**，不是矩形。小数出现的频率远高于大数。**绝不能简单相乘**。

### 💀 错误二：算法退化

* **场景：** 实现筛法时。
* **我的操作：** 写了一个函数单独去算每个数的约数，然后在循环里一个个调用它。
    ```python
    # 错误代码示范
    for j in range(1, L):
        prefix[j] = find_divisors(j) # 导致总复杂度退化回 O(N^2)!
    ```
* **修正：** 筛法必须是通过倍数关系 **同时处理所有数字**，而不是一个一个算。

### 💀 错误三：Python 作用域错误

* **我的操作：** `for i in range(i, L, i):` (在 range 参数里使用了未定义的 `i`)。
* **修正：** 必须使用外层循环的变量（如 `factor`）作为起始点和步长：`for i in range(factor, L, factor):`。

---

## 4.正确答案
```python
   import sys

# 设置递归深度并不是必须的，但为了好习惯留着，本题不需要递归
sys.setrecursionlimit(2000)

def solve():
    try:
        # 输入 L
        line = sys.stdin.readline()
        if not line: return
        L = int(line.strip())
    except ValueError:
        return

    MOD = 10**9 + 7 # 注意：Python里写 1e9+7 得到的是浮点数，要用整数写法

    # ---------------------------------------------------------
    # 第一步：筛法预处理 (Sieve)
    # 目标：算出每个面积 area 对应的所有矩形半周长之和
    # 复杂度：O(L log L)
    # ---------------------------------------------------------
    # energy[i] 表示面积为 i 的所有矩形的 (长+宽) 之和
    energy = [0] * (L + 1)
    
    for w in range(1, L + 1):
        # area 从 w 开始，每次增加 w (w, 2w, 3w...)
        # 这里的 area 就是当前矩形的面积，w 是宽
        for area in range(w, L + 1, w):
            h = area // w      # 算出高
            weight = w + h     # 半周长
            energy[area] += weight

    # ---------------------------------------------------------
    # 第二步：前缀和 (Prefix Sum)
    # 目标：为了快速算出 1 到 k 范围内所有 energy 的和
    # 复杂度：O(L)
    # ---------------------------------------------------------
    # prefix_E[i] = energy[1] + ... + energy[i]
    prefix_E = [0] * (L + 1)
    for i in range(1, L + 1):
        # 记得一边加一边取模，防止数字过大（虽然Python不怕大数，但取模快一点）
        prefix_E[i] = (prefix_E[i-1] + energy[i]) % MOD

    # ---------------------------------------------------------
    # 第三步：统计答案 (Optimization)
    # 目标：u * v <= L，利用除法消灭内层循环
    # 复杂度：O(L)
    # ---------------------------------------------------------
    ans = 0
    
    # 枚举矩形 A 的面积 u
    for u in range(1, L + 1):
        # 根据 u * v <= L，算出 v 的最大值
        max_v = L // u
        
        # 既然 v 可以取 1 到 max_v 的任意值
        # 那么 v 的所有能量之和就是 prefix_E[max_v]
        sum_v_energy = prefix_E[max_v]
        
        # 累加答案：(u 的能量) * (v 能量的总和)
        # 注意取模
        term = (energy[u] * sum_v_energy) % MOD
        ans = (ans + term) % MOD

    print(ans)

solve()
```

---

## 5. 心得总结 (Summary)

1.  **逆向思维 (Inverse Thinking)：** 不要去拆解复杂的合数，要去聚合简单的因子。
2.  **建模先行 (Model First)：** 写代码本质上只是在翻译数学公式。如果公式没推出来，写出来的代码就是垃圾。
3.  **建立“工具箱” (The Toolbox)：**
    * 遇到 变量联动 $\rightarrow$ **前缀和**
    * 遇到 约数/倍数 $\rightarrow$ **调和级数筛**
    * 遇到 约束问题 $\rightarrow$ **数学建模**

> "不是要现场发明数学，而是要识别模型，调用工具。"
