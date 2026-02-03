# [算法笔记] 最小生成树进阶：连接所有点的最小费用（Kruskal 解法）

## 1. 题目模型与定义

**题目描述：**  
给定平面上 $N$ 个点的坐标 $(x_i, y_i)$，任意两点之间均可连接，连接费用为两点间的曼哈顿距离：$|x_i - x_j| + |y_i - y_j|$。求将所有点连接成一个连通图所需的最小总费用。

**问题本质：**  
这是一个典型的**最小生成树 (Minimum Spanning Tree, MST)** 问题。与常规图论题不同，本题未直接给出边（Edge），只给出了点（Vertex）。此类问题称为**隐式图 (Implicit Graph)** 问题，需要先根据规则构建出边，再进行算法求解。

---

## 2. 核心知识点

### A. 最小生成树 (MST)
*   **定义**：在一个加权连通图中，选择 $N-1$ 条边，使得所有 $N$ 个节点互相连通，且这些边的权值之和最小。
*   **特性**：
    1.  无环 (Acyclic)。
    2.  连通 (Connected)。
    3.  包含所有节点。

### B. 距离衡量：曼哈顿距离 vs 欧几里得距离
*   **曼哈顿距离**：$d = |x_1 - x_2| + |y_1 - y_2|$（只能横平竖直走）。
*   **欧几里得距离**：$d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$（直线距离）。
*   *注意*：对于 MST 算法而言，距离公式仅影响边的“权重”数值计算，不影响算法逻辑。

### C. 时间复杂度估算
*   **边数计算**：$N$ 个点两两互连，总边数 $M = \frac{N(N-1)}{2}$。
*   **Kruskal 适用性**：当 $N \le 1000$ 时，$M \approx 5 \times 10^5$。排序复杂度 $O(M \log M) \approx 10^7$ 次运算，在竞赛时限（1秒）的安全范围内。

---

## 3. 错误思路复盘

在解题过程中常见的两种典型错误思维与实现漏洞：

### 错误思路一：最近邻居贪心法 (Local Greedy)
*   **思路描述**：遍历每个节点，只寻找离该节点最近的一个点进行累加。即 `result += min(dist[i])`。
*   **逻辑缺陷**：
    1.  **连通性缺失**：每个点只负责找离自己最近的点，可能导致形成多个互不相连的封闭小圈子（例如 A 连 B，B 连 A；C 连 D，D 连 C，但 AB 与 CD 不通）。
    2.  **方向限制**：若仅遍历 `range(i, N)`，会导致排序靠后的节点无法选择之前的节点，破坏了全局最优性。
*   **结论**：最小生成树必须基于**“全局边排序”（Kruskal）**或**“集合扩张”（Prim）**，不能基于单点的局部最优。

### 错误思路二：数据结构与语法实现漏洞
*   **二维列表误用**：试图构建 `dist[i]` 并使用 `append` 添加三个参数 `(d, i, j)`。
    *   *纠正*：`list.append()` 仅接受一个参数；Kruskal 只需要一个扁平的一维列表存储所有边，形式为 `[(cost, u, v), ...]`。
*   **变量名拼写错误**：在 `union` 函数中混用 `root_Y` 与 `root_y`。
    *   *影响*：导致 `NameError`。

---

## 4. 正确解题逻辑 (Kruskal 算法流程)

### Step 1: 构造边 (Build Edges)
由于是隐式图，首先需要通过双重循环遍历所有点对 $(i, j)$，计算曼哈顿距离，并将边信息以元组形式 `(distance, u, v)` 存入列表 `edges`。
*   **技巧**：内层循环从 `i + 1` 开始，避免重复计算（无向图对称性）和自环。

### Step 2: 排序 (Sort)
对 `edges` 列表进行**升序排序**。
*   **目的**：保证贪心策略的有效性，优先选择成本最低的边。

### Step 3: 遍历与合并 (Union-Find)
初始化并查集（DSU），包含 `parent` 数组和连通分量计数器 `count`。
1.  **查找**：使用 `find(u)` 和 `find(v)` 判断两点是否已连通。
2.  **判定**：
    *   若**已连通**（父节点相同）：跳过该边（避免成环）。
    *   若**未连通**：执行 `union`，将 `distance` 累加至总费用，并将连通分量 `count - 1`。
3.  **终止**：当 `count == 1` 或已合并 $N-1$ 条边时，可提前结束循环。

---

## 6. 正确答案板块 (Correct Solution)

```python
import sys
# 1. 递归深度设置好
sys.setrecursionlimit(200000)

data = map(int, sys.stdin.read().split())
iterator = iter(data) # 把它转成迭代器更稳妥

try:
    N = next(iterator)
except StopIteration:
    exit()

li = []
for _ in range(N):
    x = next(iterator)
    y = next(iterator)
    li.append([x, y])

# --- 修正点 1：造边 ---
dist = []
for i in range(N):
    for j in range(i + 1, N):
        d = abs(li[i][0] - li[j][0]) + abs(li[i][1] - li[j][1])
        # 直接往大列表里 append 一个元组 (距离, u, v)
        dist.append((d, i, j))

# 排序
dist.sort()

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.count = n
        
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
        
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            # --- 修正点 2：大小写拼写修正 ---
            self.parent[root_x] = root_y 
            self.count -= 1
            return True
        return False

dsu = DSU(N)
result = 0
edges_count = 0 # 可选：加个计数器辅助判断

for d, u, v in dist:
    if dsu.union(u, v):
        result += d
        edges_count += 1
    
    # 剪枝：如果只剩1个连通分量，或者已经连了 N-1 条边，都可以提前退出
    if dsu.count == 1:
        break

print(result)
```
## 5. 总结
1.  **从点到图**：对于没给边的题目，第一步永远是根据规则把“点”转化成“边列表”。
2.  **算法选择**：
    *   **Kruskal**：适合 $N$ 较小或边较少的场景，核心是 “边排序 + 并查集”。逻辑清晰，不易出错。
    *   **Prim**：适合 $N$ 较大且边非常稠密的场景，核心是 “堆 + visited数组”。
3.  **调试习惯**：涉及列表操作时，注意维度；涉及类内部变量时，注意 `self` 和大小写拼写。

---

