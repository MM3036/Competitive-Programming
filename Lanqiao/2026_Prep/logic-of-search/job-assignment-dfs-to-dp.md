## 📘 算法进阶笔记：从 DFS 到 动态规划 (DP)

**课题：** 工程分配问题 (Job Assignment Problem)  
**核心线索：** 递归机制 $\rightarrow$ 剪枝优化 $\rightarrow$ 位运算压缩 $\rightarrow$ 记忆化搜索

---

### 1. 🏛️ 题目场景

**背景：** 你是项目经理，有 $N$ 名员工和 $N$ 项工程。每名员工做不同工程的报价不同（Cost Matrix）。  
**目标：** 给每名员工分配一项工程（一一对应，不可重复），使得 **总花费最小**。

#### 成本矩阵数据示例 (N=3)：

| 员工 \ 工程 | 工程 0 | 工程 1 | 工程 2 |
| :--- | :---: | :---: | :---: |
| **员工 A (0)** | 10 | 20 | 5 |
| **员工 B (1)** | 15 | 10 | 10 |
| **员工 C (2)** | 30 | 5 | 20 |

---

### 2. 🌲 第一阶段：DFS 与 回溯机制 (The Mechanism)

**核心领悟：**
- **递归 (Recursion)**：是**机制**。函数调用自身 + 系统栈存储局部变量。
- **DFS (深度优先搜索)**：是**策略**。不撞南墙不回头，一条路走到黑。
- **回溯 (Backtrack)**：是**动作**。撤销当前选择，恢复现场，去寻找其他可能。

#### 📝 思考练习 1：DFS 结构
在普通 DFS 中，通常用一个 `visited` 数组来记录工程占用情况。

```python
# 伪代码结构
def dfs(person_id, current_cost):
    # 1. 终止条件
    if person_id == N:
        update_global_min(current_cost)
        return

    # 2. 遍历所有工程
    for job_id in range(N):
        # A. 检查：这个 job_id 是否被占用了？
        if not visited[job_id]:
            # B. 标记占用 (进门)
            visited[job_id] = True
            # C. 递归进入下一层
            dfs(person_id + 1, current_cost + cost_matrix[person_id][job_id])
            # D. 回溯 (出门) -> 恢复现场
            visited[job_id] = False
```

---

### 3. ✂️ 第二阶段：剪枝策略 (Pruning)

DFS 的效率取决于“剪树枝”的狠度：

- **A. 可行性剪枝 (Feasibility)**：
    - 含义：这条路违规了（如工程冲突），不能走。
    - 实现：通过 `visited` 数组判断。
- **B. 最优性剪枝 (Optimality)**：
    - 含义：这条路虽然合规，但太贵了，肯定不如已找到的解。
    - 实现：维护全局最小 `ans`。如果 `current_cost >= ans`，直接 `return`。

**💡 关键 Q&A：**
- **Q:** `float('inf')` 是什么？  
  **A:** 正无穷大。用于初始化最小值，确保第一个有效解能成功更新 `ans`。
- **Q:** 手动设一个 `ans = 40` (人工上界) 行吗？  
  **A:** 行，这叫启发式上界。**风险**是如果最优解大于 40，你会错过它。必须确保该上界是真实可达的。

---
##  代码实现 (Python)

```python
# 数据定义
pre_data = [
    [10, 20, 5],  # 员工 A
    [15, 10, 10], # 员工 B
    [30, 5, 20]   # 员工 C
]
data = [0] * 3    # 记录每个人的选择
ans = 40          # 初始上界 (Upper Bound)，用于辅助剪枝

def check(row, col):
    """
    检查列冲突：判断工程 col 是否已经被之前的员工 (0 到 row-1) 选过了
    """
    for i in range(row):
        if data[i] == col:
            return False
    return True

def dfs(n, current_money):
    """
    n: 当前正在处理第几个员工
    current_money: 当前累积的花费
    """
    global ans
    
    # --- 最优性剪枝 (Optimality Pruning) ---
    # 如果当前花费已经超过已知最优解，止损
    if current_money >= ans:
        return

    # --- Base Case: 递归终止 ---
    # 所有员工都分配完毕
    if n == 3:
        ans = current_money
        return

    # --- 横向遍历所有选择 ---
    for i in range(3): # 尝试分配工程 0, 1, 2
        
        # 1. 可行性检查
        if check(n, i):
            data[n] = i # 记录路径
            
            # 2. 预测性剪枝 (进入下一层前的最后确认)
            new_cost = current_money + pre_data[n][i]
            if new_cost < ans:
                dfs(n + 1, new_cost)
            
            # 回溯：因为 data[n] 会在下一次循环被覆盖，
            # 且 check 只检查 n 之前的行，所以此处无需显式重置状态。

# --- 主程序 ---
if __name__ == "__main__":
    dfs(0, 0)
    print(f"最小花费是: {ans}")
    # 预期输出: 25 (路径: A->2, B->1, C->1[冲突] -> 回溯 -> A->2, B->0, C->1)
```

### 4. 🧬 第三阶段：位运算与状态压缩 (Bitmask)

**核心领悟：** 位运算是状态压缩的手段，将布尔数组压缩成一个**整数**。

#### 🛠️ 必须掌握的“三套连招”
假设 `mask` 是当前状态（整数），`i` 是第 $i$ 号工程。

| 动作 | 目的 | 代码咒语 (Python) | 解析 |
| :--- | :--- | :--- | :--- |
| **定位** | 制造第 $i$ 位的工具 | `1 << i` | 将 1 向左移动 $i$ 位 |
| **检查** | 看第 $i$ 位是否为 1 | `(mask >> i) & 1` | 右移后与 1 做“与”运算 |
| **标记** | 把第 $i$ 位变成 1 | `mask \| (1 << i)` | 按位“或”运算，强制变 1 |

**📝 思考练习 2：**
如果 `mask = 5` (二进制 `101`)，代表 0、2 号工程被占用。
欲占用 1 号工程：`101 | 010` $\rightarrow$ `111` (十进制 7)。

---

### 5. 🧠 第四阶段：记忆化搜索 (DP) —— 核武器

**痛点：** DFS 记性不好，同样的局面（剩下的人和工程一样）会重复计算无数次。  
**关键：** `mask` 变成了整数，可以作为字典或数组的 `Key`。

#### 🔄 逻辑反转 (从 Void 到 Return)
- **旧 DFS**：我是会计，带着账本跑。参数变动多，缓存难命中。
- **DP 态 DFS**：我是老板，问下属：`dfs(n, mask)` —— “把剩下的活干完，最少还要多少钱？”

```python
memo = {} 

def dfs(n, mask):
    # 1. 查备忘录
    if (n, mask) in memo: return memo[(n, mask)]

    # 2. Base Case
    if n == N: return 0

    min_val = float('inf')
    
    # 3. 状态转移
    for i in range(N):
        if not ((mask >> i) & 1): # 如果工程 i 未被占用
            # 当前成本 + 解决子问题的最小成本
            cost = cost_matrix[n][i] + dfs(n + 1, mask | (1 << i))
            min_val = min(min_val, cost)
    
    # 4. 记账
    memo[(n, mask)] = min_val
    return min_val
```

---

### 6. 🚀 第五阶段：Python 实战技巧 (@lru_cache)

- **`@lru_cache(None)`**：Python 标准库自带的装饰器，自动管理 `memo`。
- **⚠️ 避坑指南**：
    1. 不要加在有全局累加变量（无返回值）的函数上。
    2. 函数返回值必须完全取决于输入参数。
    3. **递归深度**：Python 默认限制 1000。
       ```python
       import sys
       sys.setrecursionlimit(200000)
       ```
- **效率**：从 $O(N!)$ 优化到 $O(N \cdot 2^N)$。这是“降维打击”。

---

### 7. 🌟 总结：你的算法进化路线

1. **看山是山**：写出循环暴力解（层数不确定，宣告失败）。
2. **看山不是山**：学会 **DFS 递归**，把问题看作一棵树。
3. **看山是树**：学会 **剪枝**，砍掉枯枝败叶。
4. **看树是数**：学会 **位运算**，把数组压成整数。
5. **万法归一**：学会 **DP**，用空间换时间，消除重复计算。

---
