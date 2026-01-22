按照您的要求，我将上述完整内容整理为标准的 GitHub Flavored Markdown 格式，保持文字内容不变，优化排版结构。

***

# [算法笔记] 网格 DFS 与 Flood Fill：代号污染源

> **题目来源**：代号：污染源 (The Contaminated Zones)  
> **核心标签**：`DFS` `Flood Fill (洪水填充)` `连通性判断` `沉岛思想`  
> **难度**：Easy-Medium (网格搜索入门必修)

## 1. 题目简述

给定一个由 `0` (安全) 和 `1` (污染) 组成的二维矩阵。要求计算图中面积最大的那一片连通污染区包含多少个格子。连通定义为上下左右四个方向相邻。

## 2. 标准代码实现 (Industrial Strength)

这是修正了语法错误、边界检查顺序，并采用“沉岛思想”优化的最终版本。

```python
import sys

# 1. 设置递归深度
# Python 默认递归深度约 1000，而在极端地图（如蛇形走位）下可能不够用
# 遇到 DFS 题，起手先开大递归限额，防止 RecursionError
sys.setrecursionlimit(20000)

def solve():
    # 读取输入处理 (根据具体平台调整)
    input_data = sys.stdin.read().split()
    if not input_data: return
    iterator = map(int, input_data)
    
    try:
        M = next(iterator) # 行数 (Rows)
        N = next(iterator) # 列数 (Cols)
    except StopIteration: return

    # 构造矩阵
    maze = []
    for _ in range(M):
        row = [next(iterator) for _ in range(N)]
        maze.append(row)

    # 方向数组：上下左右 (顺序在求面积时不影响结果)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # -------------------------------------------------
    # 核心 DFS 函数：负责“清除”并统计一片区域
    # -------------------------------------------------
    def dfs(r, c):
        # 【边界守卫 (Guard Clause)】
        # 必须先判断越界，再判断是否为 0。顺序反了会报错 (IndexError)。
        if not (0 <= r < M and 0 <= c < N) or maze[r][c] == 0:
            return 0
        
        # 【沉岛思想 (Sinking Island)】
        # 标记已访问：直接修改原数组，将 1 变为 0。
        # 既防止了无限循环 (A走到B，B又走回A)，又省去了 visited 数组的空间。
        maze[r][c] = 0
        
        # 统计面积：当前格子(1) + 四周延伸的面积
        area = 1
        for dr, dc in directions:
            area += dfs(r + dr, c + dc)
            
        return area

    # -------------------------------------------------
    # 主架构：扫描全图
    # -------------------------------------------------
    max_area = 0
    # 两层循环遍历每一个格子 (地毯式搜索)
    for i in range(M):
        for j in range(N):
            if maze[i][j] == 1:
                # 一旦发现新大陆，立即派 DFS 去丈量并铲平它
                current_area = dfs(i, j)
                if current_area > max_area:
                    max_area = current_area
                    
    print(max_area)

if __name__ == "__main__":
    solve()
```

## 3. 核心架构本质：先循环 vs 再递归

初学者常纠结：“为什么有两层循环还要递归？这不慢吗？”。这其实是两种不同的职能分工：

### 3.1 外层循环 (The Scanner)

```python
for i in M: for j in N
```

*   **职责**：**定位入口**。它就像卫星扫描，负责找到每一个未被发现的污染区。
*   **特性**：因为有 `maze[i][j] == 1` 的判断，且 DFS 会把处理过的 `1` 变成 `0`，所以同一个污染区只会被主循环触发一次。

### 3.2 内层递归 (The Explorer)

```python
dfs(r, c)
```

*   **职责**：**扩散销毁**。一旦主循环找到了入口，DFS 就负责顺藤摸瓜，把这整片连通区域全部走完，并标记为已处理。

### 3.3 复杂度分析

*   **误区**：认为两层循环 + 递归 = $O(N^3)$ 或更高。
*   **真相**：$O(M \times N)$ (**线性复杂度**)。
*   **原理**：虽然代码缩进很深，但每个格子一生只会被访问常数次（主循环看一次，DFS 进一次）。这就像戳泡泡纸，虽然动作多，但泡泡总数是固定的。

## 4. 关键顿悟与避坑 (Key Insights)

### 4.1 边界守卫的“短路效应”

*   **错误写法**：`if maze[x][y] == 1 and 0 <= x < M ...`
    *   这会导致 `IndexError`，因为计算机会先尝试读取数组，而此时 `x` 可能已经是 `-1` 了。
*   **正确写法**：`if 0 <= x < M ... and maze[x][y] == 1`
    *   利用逻辑与 (`and`) 的**短路特性**：如果坐标越界，直接停止判断，不会去触碰数组。

### 4.2 递归的“汇报机制”

代码中的 `area += dfs(next_r, next_c)` 是递归的精髓。这是一种分级管理：当前节点不需要知道整个岛有多大，它只需要知道“我的下属（四周）一共统计了多少”，加上“我自己（1）”，然后向上级汇报。这比使用全局变量 `global` 更安全、逻辑更清晰。

### 4.3 方向数组的顺序

在计算连通面积或岛屿数量时，`directions` 的顺序（上下左右 vs 下上右左）不影响结果。就像数葡萄，先数左边还是先数右边，葡萄的总数是不变的。

### 4.4 递归深度 (Recursion Limit)

*   **现象**：代码逻辑正确，但提交后报错 `RecursionError` 或 `Runtime Error`。
*   **原因**：地图过大或路径过长（如蛇形走位），导致递归层数超过 Python 默认限制（通常是 1000 层）。
*   **解法**：手动调用 `sys.setrecursionlimit()` 调高上限。

---

> **总结**：网格题的标准解法 = 主循环定位 (Scanner) + DFS/BFS 扩散 (Explorer) + 沉岛标记 (Marker)。掌握这一套，能解决 80% 的岛屿类问题。
