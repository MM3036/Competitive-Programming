# 差分数组算法详解：高效区间修改与还原

## 一、 题目概述

**核心任务**：在一个长度为 $N$ 的数组（初始全为 0）上，执行 $M$ 次区间修改操作。每次操作将区间 $[L, R]$ 内的所有元素增加 $V$。最后输出修改后的完整数组。

*   **算法本质**：差分数组（Difference Array）。利用差分与前缀和的互逆关系，将 $O(N)$ 的区间修改降维为 $O(1)$ 的端点修改。
*   **复杂度要求**：
    *   修改阶段时间复杂度：$O(M)$
    *   还原阶段时间复杂度：$O(N)$
    *   总时间复杂度：$O(M + N)$
    *   空间复杂度：$O(N)$

---

## 二、 核心直觉：“攒一波”策略 (Lazy Propagation Intuition)

*   **笨办法（暴力法）**：类似于“每天有一点灰尘就打扫全屋”。每次操作都遍历区间 $[L, R]$ 进行修改，耗时极高，做大量重复劳动。
*   **差分法**：类似于“每天只记录灰尘增量，月底一次性彻底打扫”。
    *   **平时（修改阶段）**：只在差分数组（账本）上记录起止点的变化（$O(1)$），极速响应。
    *   **月底（还原阶段）**：利用前缀和（扫把）从头到尾遍历一次，将所有积累的增量一次性结算应用到原数组（$O(N)$）。
*   **效益**：极大地节省了中间频繁操作的时间成本。

---

## 三、 代码失误分析

在工程实现上，常见的待修正点如下：

1.  **输出格式错误 (Output Format Error)**
    *   *现象*：直接输出列表或使用 `sys.stdout.write(''.join(str(prefix_sum)))`。
    *   *后果*：输出包含方括号和逗号，不符合 OJ（在线评测系统）要求的“空格分隔纯数字”格式。
    *   *修正*：使用 `' '.join(map(str, result))`。

2.  **前缀和还原越界风险 (Boundary Logic Risk)**
    *   *现象*：还原循环从 `i=0` 开始并访问 `prefix_sum[i-1]`。
    *   *风险*：逻辑不严谨，虽因 Python 特性可能不报错，但易引发思维混乱。
    *   *修正*：索引从 1 开始，或使用一个辅助变量累加。

3.  **空间冗余 (Space Inefficiency)**
    *   *优化*：无需开辟额外的 `prefix_sum` 数组，直接在差分数组上进行**原地前缀和计算**（In-place Prefix Sum），可节省 $O(N)$ 空间。

---

## 四、 核心知识点回顾

### 1. 差分数组定义
构造数组 $D$，使得原数组 $A$ 是 $D$ 的前缀和：
$$A[i] = \sum_{k=1}^{i} D[k]$$

### 2. 区间修改原理
若要将区间 $[L, R]$ 内所有元素加上 $V$，只需修改差分数组的两个端点：
*   **起点（开始增加）**：$D[L] \leftarrow D[L] + V$
*   **终点后一位（停止增加）**：$D[R+1] \leftarrow D[R+1] - V$

### 3. 算法流程
1.  **初始化**：建立大小为 $N+2$ 的差分数组（多出的空间防止 $R+1$ 越界）。
2.  **记账（修改）**：读入 $M$ 次指令，执行 $O(1)$ 的端点记录。
3.  **大扫除（还原）**：对差分数组求前缀和，一次性恢复出原数组 $A$。
4.  **输出**：格式化输出结果。

---

## 五、 正确代码实现 (Correct Answer)

以下是基于上述逻辑的最优 Python 实现：

```python
import sys

def solve():
    # 使用快速读入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx])
    M = int(input_data[idx + 1])
    idx += 2
    
    # 1. 初始化差分数组 (长度 N+2 防止 R+1 越界)
    # 假设 L, R 是从 1 到 N 的坐标
    diff = [0] * (N + 2)
    
    # 2. 修改阶段：O(1) 记账
    for _ in range(M):
        L = int(input_data[idx])
        R = int(input_data[idx + 1])
        V = int(input_data[idx + 2])
        idx += 3
        
        diff[L] += V
        diff[R + 1] -= V
    
    # 3. 还原阶段：O(N) 原地前缀和计算
    result = []
    current_val = 0
    for i in range(1, N + 1):
        current_val += diff[i]
        result.append(current_val)
    
    # 4. 格式化输出
    sys.stdout.write(' '.join(map(str, result)) + '\n')

if __name__ == "__main__":
    solve()
```
