### 算法笔记：一维前缀和与 Python 竞赛技巧

#### 1. 题目模型：区间权值查询 (Interval Sum)

*   **题目描述**：给定一个长度为 $N$ 的整数数组 $A$（下标从 1 开始）。随后进行 $M$ 次询问，每次询问给出一个闭区间 $[l, r]$，求该区间内所有元素的和。
*   **输入格式**：
    *   第一行：$N, M$
    *   第二行：$N$ 个整数（数组元素）
    *   接下来 $M$ 行：每行两个整数 $l, r$
*   **核心难点**：
    *   **朴素算法**：每次遍历求和 $O(N)$，总复杂度 $O(N \times M)$。当 $N, M$ 达到 $10^5$ 级别时会超时 (TLE)。
    *   **优化目标**：预处理 $O(N)$，查询 $O(1)$。

#### 2. 核心知识点：前缀和 (Prefix Sum)

**A. 什么是前缀和？**
定义 $S[i]$ 为数组前 $i$ 个数的和。
*   **Padding (哨兵) 技巧**：为了处理下标边界，数组长度开 $N+1$，且令 $S[0] = 0$。这样在计算 `Sum(1, r)` 时，公式 `S[r] - S[0]` 依然成立。

**B. 两个关键公式**
*   **预处理公式 (递推)**：
    $$S[i] = S[i-1] + A[i]$$
    *(当前前缀和 = 前一个前缀和 + 当前元素)*
*   **查询公式 (区间和)**：
    $$Sum(l, r) = S[r] - S[l-1]$$
    *(区间和 = 终点的前缀和 - 起点前一个位置的前缀和)*

#### 3. 实战中的 Python 疑问 (Q&A 整理)

在算法竞赛（如蓝桥杯、LeetCode、Codeforces）中，Python 的效率优化至关重要：

**Q1: 关于输入处理 (iterator vs map vs list)**
*   **`sys.stdin.read().split()`**：一次性读入所有数据到内存，比循环调用 `input()` 快得多。
*   **`iterator = iter(data)`**：创建一个指针，指向数据流的开头。
    *   *好处*：无需维护下标变量 `idx`，不用担心切片越界，调用 `next(iterator)` 即可拿到下一个数据。
*   **`map(int, ...)`**：
    *   *注意*：单纯的 `map` 是迭代器（惰性计算，省内存）；`list(map(...))` 是全打包。做纯数字题目时，直接用 `map` 生成的迭代器配合 `next()` 是最优解。

**Q2: 列表推导式 (List Comprehension) 的使用场景**
*   **扁平化 (Flatten)**：`[x for row in matrix for x in row]`。用于把二维压成一维（如全局排序、计数）。
*   **初始化可变对象**：`[[0]*M for _ in range(N)]`。
    *   *切记*：初始化二维数组时，**不能**用 `[[0]*M] * N`，否则改一个格子整列都会变（浅拷贝陷阱）。

**Q3: 索引视角 (i+1 vs i-1)**
*   **向前看 (`prefix[i+1] = ...`)**：适合遍历 0 到 $N-1$ 的原数组下标，代码写起来顺手。
*   **向后看 (`prefix[i] = prefix[i-1] + ...`)**：更符合数学直觉。
*   **结论**：建议配合 **Padding 技巧** 使用“向后看”逻辑，即原数组和前缀和数组都开 $N+1$，下标从 1 开始对应，减少脑机转换损耗。

**Q4: 输出优化 (sys.stdout.write + join)**
*   **速度**：`print()` 每次都会刷新缓冲区，慢；`sys.stdout.write()` 一次性把长字符串丢给终端，快。
*   **格式**：`'\n'.join(results)` 就像“胶水”，只涂在砖块之间。
    *   *注意*：如果不手动加最后的 `+ '\n'`，光标会停在最后一个结果后面。在某些判题系统中，缺少末尾换行可能导致格式错误。

#### 4. 你的解题 Checklist (自我检测)

**I/O**：引用 `sys`，用 `map(int, sys.stdin.read().split())` 搞定输入流。
**数组**：创建 $N+1$ 大小的 `prefix` 数组，初始全 0。
**计算**：从 1 遍历到 $N$，套用预处理公式。
**查询**：循环 $M$ 次询问，套用查询公式 `S[r] - S[l-1]`。
**输出**：将结果转为字符串存入列表，用 `sys.stdout.write` 一次性打印。

---

#### 5. 正确答案 (Code Implementation)

```python
import sys

# 1. 快速读取
input = sys.stdin.read
data = input().split()
iterator = iter(data)

N = int(next(iterator))
M = int(next(iterator))

# 2. 直接构建前缀和数组 (S[0] = 0)
# 这里为了节省一次循环，直接在列表推导式里处理
# 但为了可读性，通常分步写也是完全OK的
nums = [int(next(iterator)) for _ in range(N)]
prefix = [0] * (N + 1)
for i in range(N):
    prefix[i+1] = prefix[i] + nums[i]

# 3. 批量处理输出
results = []
for _ in range(M):
    l = int(next(iterator))
    r = int(next(iterator))
    results.append(str(prefix[r] - prefix[l-1]))

# 4. 一次性打印
sys.stdout.write('\n'.join(results) + '\n')
```

---
