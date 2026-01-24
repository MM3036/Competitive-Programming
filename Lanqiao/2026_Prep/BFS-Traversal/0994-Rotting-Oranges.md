# LeetCode 994. 腐烂的橘子 (Rotting Oranges)

## 1. 核心考点

- **多源 BFS (Multi-Source BFS)**: 
  - 与传统的单源 BFS 不同，本题的起始状态（时间 $t=0$）可能有多个“传染源”（所有初始腐烂的橘子）。
  - 需要将这些源头同时入队，模拟**并行扩散**的过程。
- **网格图遍历 (Grid Traversal)**: 
  - 处理二维矩阵的坐标变换 `(r, c)` 和边界检查 `0 <= nr < R`。
- **层序遍历 (Level-order Traversal)**: 
  - 利用队列的 **FIFO** 特性，按层处理节点。每一层代表时间流逝了 **1 分钟**。

## 2. 解题思路 (物理模型：波的传播)

**核心思想**：不要对每个腐烂橘子单独跑 BFS（那样会重复计算且超时）。应将所有初始腐烂橘子视为同一层级的**波源**，像水波纹一样同时向外扩散。

### 步骤拆解：

1.  **预处理 (Initialization)**:
    - 遍历整个网格。
    - 找到所有 **腐烂橘子 (`2`)**，将它们的坐标加入队列 `q`。
    - 同时统计 **新鲜橘子 (`1`)** 的数量 `fresh_count`。这是为了最后判断是否所有橘子都腐烂了。

2.  **BFS 循环 (The Loop)**:
    - 只要队列不为空 **且** 还有新鲜橘子 (`fresh_count > 0`)，就继续循环。
    - **快照机制 (Snapshot)**: 
      - 在每一轮循环开始时，记录当前队列长度 `n = len(q)`。
      - 这 `n` 个节点代表当前这一分钟的所有传染源。
      - 仅处理这 `n` 个节点，确保时间 `minutes` 的增加是按层计算的。
    - **扩散**: 
      - 取出节点，向上下左右四个方向检查。
      - 如果碰到新鲜橘子：
        1.  将其标记为腐烂 (`grid[nr][nc] = 2`)。
        2.  `fresh_count` 减 1。
        3.  加入队列（作为下一分钟的传染源）。

3.  **结果校验 (Validation)**:
    - 循环结束后，检查 `fresh_count`：
      - 如果为 `0`：说明所有能腐烂的都腐烂了，返回 `minutes`。
      - 如果 `> 0`：说明有橘子被空白格隔离，无法被波及，返回 `-1`。

## 3. 复杂度分析

- **时间复杂度**: $O(N \times M)$
  - $N$ 和 $M$ 分别是网格的行数和列数。
  - 每个网格点最多进队一次、出队一次。
- **空间复杂度**: $O(N \times M)$
  - 最坏情况下（例如所有橘子都是腐烂的），队列可能需要存储网格中所有的点。

## 4. 代码实现 (Python)

```python
from collections import deque
from typing import List

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        R, C = len(grid), len(grid[0])
        q = deque()
        fresh_count = 0
        
        # Step 1: 初始化
        # 扫描全图，将所有初始腐烂橘子入队，并统计新鲜橘子数量
        for r in range(R):
            for c in range(C):
                if grid[r][c] == 1:
                    fresh_count += 1
                elif grid[r][c] == 2:
                    q.append((r, c))
        
        # 边界情况优化：如果没有新鲜橘子，直接返回 0
        if fresh_count == 0:
            return 0
        
        minutes = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        # Step 2: 多源 BFS 主循环
        # 注意条件：q 不为空 且 还有新鲜橘子
        while q and fresh_count > 0:
            # 记录当前层级的节点数量（当前这一分钟要扩散的源头）
            n = len(q)
            
            # 处理当前层的所有节点
            for _ in range(n):
                r, c = q.popleft()
                
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    
                    # 检查边界及是否为新鲜橘子
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                        grid[nr][nc] = 2      # 关键：立即标记为腐烂 (避免重复访问)
                        fresh_count -= 1      # 更新剩余新鲜橘子计数
                        q.append((nr, nc))    # 加入队列，作为下一轮的源头
            
            # 当前层处理完毕，时间 +1
            minutes += 1
            
        # Step 3: 结果返回
        # 如果还有新鲜橘子剩余，说明无法完全腐烂
        if fresh_count > 0:
            return -1
        else:
            return minutes
```

## 5. 常见误区 (Pitfalls)

1.  **时间计算错误**:
    - ❌ 错误写法：每处理一个节点 `minutes += 1`。
    - ✅ 正确写法：每处理完 **一层** (`range(len(q))`) 节点，`minutes += 1`。
2.  **重复访问 / 死循环**:
    - 必须在将橘子加入队列的同时将其标记为腐烂 (`grid[x][y] = 2`)。
    - 如果等到出队时才标记，同一个新鲜橘子可能被多个相邻的腐烂橘子重复加入队列，导致超时。
3.  **循环结束条件**:
    - 如果队列还不为空，但 `fresh_count` 已经是 0 了，其实可以提前结束，避免多加一次无用的时间（虽然本题逻辑中最后一次层序遍历如果没感染新橘子不会增加 minutes，但加上 `fresh_count > 0` 判断更严谨）。
4.  **冗余搜索**:
    - 不需要对每个腐烂橘子单独运行 BFS。所有源头应在初始时一起入队。
```
