# [蓝桥杯笔记] 并查集基础：省份数量 / 连通块统计

## 1. 题目模型
**关键词**：连通性、朋友圈、亲戚关系、省份数量、独立团伙个数。  
**核心问题**：给你一堆点和它们之间的连接关系，问最后分成了几个独立的集合？

## 2. 解题思路：为什么用并查集？
*   **BFS/DFS**：需要遍历每个点。如果图是不连通的，需要多次启动搜索并维护 `visited` 数组，代码逻辑相对繁琐。
*   **并查集 (DSU)**：
    *   **初始化**：一开始有 $N$ 个点，默认就有 $N$ 个独立团伙（`self.count = n`）。
    *   **合并**：每当读入一条有效的连接关系（即两个点原本属于不同集合），就执行 `union`，同时团伙数量减 1（`self.count -= 1`）。
    *   **结果**：最后剩下的 `self.count` 即为答案。

## 3. 难点攻克：邻接矩阵输入
在蓝桥杯（ACM模式）中，题目常给出 $N \times N$ 的邻接矩阵，实际输入是控制台里的 $N$ 行数字。

**转换与优化技巧**：
1.  **矩阵对称性**：A 连 B 等于 B 连 A。
2.  **减少冗余**：在遍历矩阵建立关系时，不需要遍历整个 $N \times N$，只需要遍历**右上半区**（即 `j` 从 `i + 1` 开始）。
    *   避免重复检查（0连1查一遍，1连0又查一遍）。
    *   避免无效自环（对角线 `i == j` 逻辑上不改变连通性）。

## 4. Python 竞赛满分模板

```python
import sys

# 【必写】防止递归爆栈，蓝桥杯 Python 解题一定要加
sys.setrecursionlimit(200000)

class DSU:
    def __init__(self, n):
        # 每个人父节点初始为自己
        self.parent = list(range(n)) 
        # 【核心】初始连通分量数 = 节点总数
        self.count = n               

    def find(self, x):
        """查找 + 路径压缩 (Path Compression)"""
        if self.parent[x] != x:
            # 递归向上找，并把沿途所有点的父节点直接设为根节点
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """合并两个集合"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        # 如果老大不同，说明原本不是一伙的，合并！
        if root_x != root_y:
            self.parent[root_x] = root_y
            # 【核心】合并成功，连通分量少一个
            self.count -= 1          

def solve():
    # 1. 读取节点数量 N
    try:
        line = sys.stdin.readline()
        if not line: return
        n = int(line.strip())
    except ValueError: 
        return

    dsu = DSU(n)

    # 2. 读取并解析邻接矩阵
    for i in range(n):
        # 读入当前这一行 (Row i)
        row = list(map(int, sys.stdin.readline().split()))
        
        # 遍历这一行，寻找连接关系
        # j 从 i + 1 开始，只看右上半区，跳过对角线和重复项
        for j in range(i + 1, n):
            if row[j] == 1:
                dsu.union(i, j)

    # 3. 输出剩下的团伙数量
    print(dsu.count)

if __name__ == "__main__":
    solve()
```

## 5. 避坑指南 (Tips)
1.  **路径压缩是必须的**：`find` 函数中 `self.parent[x] = self.find(...)` 必须背下来，否则在大数据量（如 $10^5$ 级）下会触发超时（TLE）。
2.  **下标偏移**：题目如果给的是城市 $1$ 到 $N$，但代码习惯用 $0$ 到 $N-1$。读取输入时记得根据情况进行 `-1` 操作或者开 `N + 1` 的空间。
3.  **递归深度**：Python 默认递归深度很浅（约 1000），碰到链状数据结构会报错，务必在开头添加 `sys.setrecursionlimit`。
4.  **读取性能**：对于大规模数据，使用 `sys.stdin.readline` 比 `input()` 快得多。

---
