# LeetCode 1162. 地图分析 - 多源 BFS 的逆向思维

## 1. 核心考点：源头的战略选择

这道题最容易让人掉进**“直觉陷阱”**。

*   **陷阱直觉**：题目问“海洋到陆地的距离”，所以我应该遍历每一个海洋 `(0)`，去搜最近的陆地。
*   **工程现实**：海洋是未知的，陆地是已知的。信息（距离）必须从已知流向未知。
*   **正确策略**：把所有陆地 `(1)` 扔进队列，让它们像**填海造陆**一样，向海洋扩散。

## 2. 物理模型：领土扩张 (Territory Expansion)

*   **初始状态 ($t=0$)**: 所有陆地同时开始向外扩张。
*   **$t=1$**: 紧贴着陆地的第一圈海洋被“占领”，标记距离。
*   **$t=k$**: 第 $k$ 圈波浪到达深海。
*   **终局**: 最后被占领的那块海洋，就是“离陆地最远”的地方。

## 3. 关键工程细节 (Engineering Specs)

### A. 内存复用 (In-Place Modification)
我们没有创建额外的 `dist` 矩阵，直接复用输入的 `grid`。
*   **陆地**: 值为 `1`（既是源头，又是墙壁）。
*   **海洋**: 值为 `0`（等待被写入距离）。
*   **已访问**: 只要 `grid[x][y] != 0`，说明已经被更近的陆地占领了，跳过。

### B. 坐标系校准 (Calibration)
*   **问题**: 题目给的陆地初始值是 `1`，而不是标准的 `0`。
*   **后果**: 我们是在“抢跑 1 米”的情况下开始计算的。
*   **修正**: 最终输出结果时，执行 `result - 1` 以消除偏差。

### C. 熔断机制 (Circuit Breaker)
*   **场景**: 地图全是陆地 或 地图全是海洋。
*   **动作**: 这种情况下 BFS 队列要么是空的，要么是满的。
*   **代码**: `if len(q) == 0 or len(q) == N*N: return -1`
*   **目的**: 防止 BFS 无意义运行，并防止输出错误答案。

## 4. 标准代码模板 (Final Code)

```python
import sys
from collections import deque

def solve():
    # 1. I/O 读取 (处理流式输入)
    input_data = sys.stdin.read().split()
    if not input_data: return
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    q = deque()
    grid = []
    
    # 2. 初始化与源头装载
    for r in range(N):
        row = []
        for c in range(N):
            val = int(next(iterator))
            row.append(val)
            if val == 1:
                q.append((r, c)) # 策略：陆地是源头
        grid.append(row)

    # 3. 边界熔断 (全是海 或 全是陆)
    if len(q) == 0 or len(q) == N * N:
        print(-1)
        return # 相当于 sys.exit(0)

    # 4. BFS 引擎
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    max_dist = -1
    
    while q:
        r, c = q.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # 边界检查
            if 0 <= nr < N and 0 <= nc < N:
                # 核心逻辑：只抢占海洋 (0)
                if grid[nr][nc] == 0:
                    grid[nr][nc] = grid[r][c] + 1  # 距离传递
                    max_dist = max(max_dist, grid[nr][nc])
                    q.append((nr, nc)) # 别忘了入队！

    # 5. 误差修正 (消除初始值 1 的影响)
    print(max_dist - 1)

if __name__ == "__main__":
    solve()
```
