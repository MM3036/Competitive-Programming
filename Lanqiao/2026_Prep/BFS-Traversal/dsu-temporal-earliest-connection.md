# [算法笔记] 并查集进阶：处理时序与权重问题

## 1. 题目模型：最早连通时刻
**题目描述**：
给定 $N$ 个节点和 $M$ 条连接记录。每条记录包含三个参数 $(t, u, v)$，表示在时刻 $t$，节点 $u$ 和节点 $v$ 建立连接。

**目标**：
计算网络中所有节点首次完全连通（即形成一个唯一的连通分量）的时间点 $T$。若遍历所有记录后仍无法完全连通，返回 -1。

**核心考点**：
*   **连通性判定**：动态维护图的连通状态（使用并查集 DSU）。
*   **贪心策略**：处理乱序数据，寻找“最早”或“最小”代价（排序/堆）。
*   **连通分量计数**：利用计数器快速判断全局连通性。

---

## 2. 核心知识点

### A. 并查集 (DSU) 的结构性优化
在此类题目中，DSU 不仅用于查找父节点，还需维护全局状态：
1.  **连通分量计数 (`count`)**：初始化为 $N$（每个节点独立）。每次成功 `union`（即两个不同集合合并）时，`count` 减 1。当 `count == 1` 时，表示图已完全连通。
2.  **路径压缩 (Path Compression)**：在 `find` 操作中递归将路径上所有节点的父节点指向根节点，保证查找复杂度接近 $O(1)$。

### B. 最小生成树 (MST) 思想雏形
本题的解题逻辑与 **Kruskal 算法** 高度一致：
*   **Kruskal 核心**：将所有边按“权重”从小到大排序，按顺序尝试合并。
*   **本题映射**：将“时间戳 $t$”视为“边的权重 $w$”。求“最早连通时刻”等同于求“**瓶颈边权重最小的生成树**”。
*   **原则**：必须先处理时间较早的边，才能保证结果的正确性。

---

## 3. 技术对比：Sort (排序) vs Heapq (堆)

| 维度 | `list.sort()` (全量排序) | `heapq` (小顶堆) |
| :--- | :--- | :--- |
| **数据处理方式** | **离线 (Offline)**：必须接收完所有 $M$ 条数据，存入列表后一次性排序。 | **在线 (Online/Streaming)**：数据可以流式读入，来一条存一条，动态维护最小值。 |
| **时间复杂度** | 排序复杂度 $O(M \log M)$，遍历过程线性。 | 建堆 $O(M)$，每次取出调整 $O(\log M)$。总最坏复杂度 $O(M \log M)$。 |
| **空间复杂度** | $O(M)$，需要完整存储所有边。 | $O(M)$，需要完整存储所有边。 |
| **优势场景** | 全量数据已知。算法竞赛（蓝桥杯/LeetCode）首选。代码简洁。 | 数据动态产生或懒加载。若只需处理前 $K$ 条边即可连通，堆可避免无效排序。 |
| **竞赛建议** | **首选**。Python 的 `sort` 经过底层优化（Timsort），通常比手动写堆操作常数更小。 | 仅在题目明确要求处理动态流数据，或内存受限无法一次性加载所有数据时使用。 |

---

## 4. 易错点与注意事项

1.  **循环边界**：必须基于 **边数 $M$** 进行循环或处理堆，而非节点数 $N$。
2.  **参数映射**：使用 `sort` 或 `heapq` 对元组 `(time, u, v)` 排序时，默认依据元组第一个元素比较。
3.  **连通性检查时机**：每执行一次成功的 `union` 后，都应立即检查 `count == 1`。若满足，当前边的时间戳即为答案。
4.  **输入输出处理**：区分 $N$ (节点数) 与 $M$ (日志数)。若循环结束仍未连通 (`count > 1`)，输出 -1。

---

## 5. 解题范式总结
此类问题的本质是 **“带权值的并查集应用”**。解题流程如下：
1.  **读取**：获取所有边信息 $(w, u, v)$。
2.  **排序**：根据题目目标（最小/最大/最早），对边进行排序。
3.  **遍历**：按顺序遍历边，使用并查集尝试合并。
4.  **判定**：在合并过程中监控连通分量数量。

---

## 6. 正确答案 (Code Implementation)

```python
import sys
import heapq

# 1. 增加递归深度，蓝桥杯必备
sys.setrecursionlimit(200000)

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.count = n # 初始连通分量为 n
        
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
        
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.count -= 1
            # 【修正点2】必须是 root_x 认 root_y 做父节点
            self.parent[root_x] = root_y 
            return True # 返回 True 表示这次合并是有效的
        return False

def solve():
    data = map(int, sys.stdin.read().split())
    iterator = iter(data)
    
    try:
        N = next(iterator)
        M = next(iterator)
    except StopIteration:
        return

    pq = []
    
    # 【修正点1】读入 M 条日志，不是 N
    for _ in range(M):
        time = next(iterator)
        a = next(iterator)
        b = next(iterator)
        # Python 默认对比元组的第一个元素(time)，所以这里直接 push 即可
        heapq.heappush(pq, (time, a, b))

    dsu = DSU(N)
    
    # 【修正点1】这里不能只循环 N 次，因为有可能处理了很多条废边才连通
    # 应该循环直到堆空了，或者中途连通了break
    while pq:
        t, x, y = heapq.heappop(pq)
        
        # 尝试合并
        dsu.union(x, y)
        
        # 【修正点3】合并完立刻检查，如果通了，当前的时间 t 就是最早时间
        if dsu.count == 1:
            print(t)
            return

    # 如果堆都空了，count 还没变成 1，说明永远无法连通
    print("-1")

if __name__ == "__main__":
    solve()

#——————————————————————————————————————————————————————————————————
logs = []
    # 既然我们要用 sort，就必须先把所有数据存到一个列表(List)里
    # 堆是来一个推一个，Sort 是先全存好再排
    for _ in range(M):
        t = next(iterator)
        u = next(iterator)
        v = next(iterator)
        logs.append((t, u, v))
    # --- 输入处理结束 ---

    # 2. 【核心】直接排序
    # Python 的 sort 默认就是对比 Tuple 的第一个元素(t)
    # 如果 t 一样，再比 u，再比 v。这里我们只关心时间 t，所以直接 sort() 即可
    # 这行代码的时间复杂度是 O(M log M)
    logs.sort()
```

---
