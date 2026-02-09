### 算法笔记：二维前缀和与 Python 优化建议

#### 一、 题目概述

*   **核心任务**：在一个 $N \times M$ 的矩阵中，高效计算 $Q$ 次任意子矩阵（由左上角坐标 $(x_1, y_1)$ 和右下角坐标 $(x_2, y_2)$ 确定）的元素之和。
*   **算法本质**：二维前缀和（2D Prefix Sum）结合容斥原理（Inclusion-Exclusion Principle）。
*   **复杂度要求**：
    *   **预处理时间复杂度**：$O(N \times M)$
    *   **单次查询时间复杂度**：$O(1)$
    *   **空间复杂度**：$O(N \times M)$

#### 二、 代码问题分析

在处理该模型时，容易出现以下三个关键错误：

1.  **维度初始化错误 (Dimension Error)**
    *   **错误表现**：使用 `[[0] * (N + 1) for _ in range(M + 1)]` 初始化数组。
    *   **后果**：构建了一个 $(M+1)$ 行、$(N+1)$ 列的矩阵，导致行列转置。当 $N \neq M$ 时，后续访问直接导致索引越界 (`IndexError`)。
2.  **索引对齐与越界 (Indexing Mismatch)**
    *   **错误表现**：原始数据使用 0-based 索引，而前缀和数组使用 Padding（1-based 索引）。
    *   **后果**：在计算公式中混用两种索引体系，导致读取数据时发生越界或逻辑错位。
3.  **查询公式逻辑错误 (Algorithmic Error)**
    *   **错误表现**：查询时错误使用 `result = P[x2][y2] - P[x1][y1]`。
    *   **后果**：这是 **一维前缀和** 的逻辑，无法处理二维区域。该公式仅减去了左上角的一个点，未能正确剔除上方和左侧的矩形区域，导致结果偏大。

#### 三、 优化与修正方案

针对上述问题，建议引入以下工程化优化策略：

**1. 空间压缩 (On-the-fly Calculation)**
*   **策略**：取消单独存储原始矩阵 `graph`。
*   **原理**：利用迭代器特性，在读取输入数据的同时直接计算前缀和 $P[i][j]$。当前位置的前缀和仅依赖于 $P[i-1][j]$、$P[i][j-1]$、$P[i-1][j-1]$ 和当前输入值 `val`。
*   **收益**：将空间占用减半，避免维护两个 $N \times M$ 的大数组。

**2. 哨兵填充 (Padding Strategy)**
*   **策略**：构建大小为 $(N+1) \times (M+1)$ 的数组，第 0 行和第 0 列全为 0。
*   **收益**：
    *   自然对齐题目给出的 1-based 坐标系。
    *   计算 $P[i][j]$ 时无需判断 $i-1$ 或 $j-1$ 是否越界。
    *   查询时可以直接使用 $x_1-1$ 和 $y_1-1$ 来表示被减去的区域边界。

**3. 二维容斥原理公式 (Correct Inclusion-Exclusion)**
*   **预处理公式**：
    $$P[i][j] = P[i-1][j] + P[i][j-1] - P[i-1][j-1] + \text{current\_val}$$
*   **查询公式**：
    $$Sum = P[x_2][y_2] - P[x_1-1][y_2] - P[x_2][y_1-1] + P[x_1-1][y_1-1]$$
    *   **解析**：
        1.  减去上方区域（$P[x_1-1][y_2]$）。
        2.  减去左侧区域（$P[x_2][y_1-1]$）。
        3.  **加回**左上角重复减去的重叠区域（$P[x_1-1][y_1-1]$）。

#### 四、 正确答案 (Code Implementation)

```python
import sys

# 1. Fast I/O Setup
input_data = sys.stdin.read().split()
iterator = map(int, input_data)

def solve():
    try:
        # 2. 读取 N, M, Q
        N = next(iterator)
        M = next(iterator)
        Q = next(iterator)
        
        # 3. 初始化二维前缀和数组 (Padding: N+1 行, M+1 列)
        # 注意：外层是行(N), 内层是列(M)
        prefix = [[0] * (M + 1) for _ in range(N + 1)]
        
        # 4. 构建前缀和矩阵
        # 优化技巧：不需要额外存储 graph 矩阵，直接读一个数算一个数
        for i in range(1, N + 1):
            for j in range(1, M + 1):
                val = next(iterator)
                # 核心公式：上方 + 左方 - 左上方 + 当前值
                prefix[i][j] = prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1] + val
        
        # 5. 处理询问
        results = []
        for _ in range(Q):
            x1 = next(iterator)
            y1 = next(iterator)
            x2 = next(iterator)
            y2 = next(iterator)
            
            # 核心查询公式（容斥原理）：
            # 右下角 - (上边界上方的大块) - (左边界左侧的大块) + (左上角重复减去的部分)
            ans = prefix[x2][y2] - prefix[x1-1][y2] - prefix[x2][y1-1] + prefix[x1-1][y1-1]
            results.append(str(ans))
        
        # 6. 批量输出
        sys.stdout.write('\n'.join(results) + '\n')
        
    except StopIteration:
        pass

if __name__ == "__main__":
    solve()
```

---
