# 03. Maze DFS: Core Logic & Optimization Notes (迷宫寻路核心笔记)

> **Summary**: 本文记录了在解决二维迷宫路径问题时，从“暴力模拟”转向“算法思维”的五个关键技术点。重点在于理解递归堆栈、变量隔离以及回溯的本质。

## 1. Direction Arrays (方向数组：工程化思维)

在处理二维网格的上下左右移动时，避免编写 4 个冗余的 `if-else` 语句。

- **The Pattern**:
  定义一个包含偏移量的列表 `options = [(0, 1), (1, 0), (0, -1), (-1, 0)]`。
- **Why**:
  配合 Python 的 **元组解包 (Tuple Unpacking)** 语法 `for dx, dy in options`，可以在一个循环内完成所有方向的尝试。
- **Benefit**:
  符合 **DRY (Don't Repeat Yourself)** 原则，逻辑统一，且易于扩展（如改为八方向移动）。

## 2. Path Immutability (路径传递：局部变量隔离)

在记录路径时，利用递归函数的 **“局部变量隔离”** 特性，避免复杂的手动回溯操作。

- **Snippet**: `dfs(x, y, path + [(x, y)])`
- **Mechanism**:
  - **`append` (Bad)**: 修改的是堆内存中**同一个**列表。回溯时必须手动 `pop`，否则会污染上一层的数据。
  - **`path + [...]` (Good)**: 每次递归调用时，都会在内存中**复印**一份全新的列表传给下一层。
- **Insight**:
  每一层递归都持有独立的路径副本，互不干扰。这相当于游戏中的“自动存档”机制，无论下一层怎么修改，本层的“存档”永远保持原样。

## 3. Boundary Checks (边界判断：门卫机制)

所有的合法性检查应在进入递归之前（或递归开头）统一处理，形成一个严密的“门卫”。

- **Order Matters (顺序至关重要)**:
  必须先判断坐标是否越界，再判断该坐标的值。利用 **短路逻辑 (Short-circuit evaluation)**。

  ```python
  # 正确顺序：先查 x,y 是否在界内，再查 maze[x][y]
  if 0 <= x < N and 0 <= y < M and maze[x][y] == 0:
      pass
## 4. Backtracking Essence (回溯：是撤销，不是折返)

理解回溯（Backtracking）的物理动作不是“走回头路”，而是 **“时光倒流”**。

- **Concept**:
  - **“去” (Forward)**: 是物理上的移动（扎猛子），进入下一层递归。
  - **“回” (Return)**: 是函数的 `return`，是 **栈帧 (Stack Frame)** 的弹出。

- **The "Teleport"**:
  当遇到死胡同，函数执行完毕，程序控制流直接跳回到上一层函数的调用点。那一层的变量（包括位置 `x, y`）依然保持着进入死胡同前的状态。你不需要“走”回来，你是直接在上一层 **“醒来”**。

- **Restoration (The Sandwich)**:
  - **进门**: `maze[x][y] = 2` (标记)。
  - **出门**: `maze[x][y] = 0` (还原)。这一步是为了让其他路径在探索时，不会被之前的死路标记误导。

## 5. Visualization (Print验证)

算法不应是黑盒，使用 `print` 辅助验证逻辑。

- **Action**:
  在 **Base Case**（终点判断）中打印 `path`。

- **Purpose**:
  不要只输出路径总数。打印完整的坐标列表能帮助大脑建立 **搜索树的视觉模型**，直观地看到每一次成功的“扎猛子”结果，验证你的构造逻辑是否正确。
```python
  # 地图数据: 0=路, 1=墙
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0]
]

# 方向数组: 右, 下, 左, 上
# 使用元组解包 (Tuple Unpacking) 简化逻辑
options = [(0, 1), (1, 0), (0, -1), (-1, 0)]
ans = 0

def dfs(r, c, path):
    global ans
    
    # --- 1. Base Case: 到达终点 ---
    if r == 4 and c == 4:
        ans += 1
        print(f'Path {ans}: {path}')
        return

    # --- 2. Mark (进门标记) ---
    # 标记当前点为 2 (已访问)，防止回头死循环
    maze[r][c] = 2

    # --- 3. Explore (循环尝试) ---
    for dx, dy in options:
        x = r + dx
        y = c + dy
        
        # [构造思维]: 先检查，再递归
        # 必须先检查越界，再查 maze 值，否则会报错 IndexError
        if 0 <= x < 5 and 0 <= y < 5:
            if maze[x][y] == 0:
                # [关键技巧]: path + new_node 生成新列表，无需回溯 path
                dfs(x, y, path + [(x, y)])
    
    # --- 4. Unmark (回溯清理) ---
    # 离开当前格前，恢复现场，允许其他路径再次访问此地
    maze[r][c] = 0

# Start Logic
print("Start exploring...")
# 初始路径包含起点
dfs(0, 0, [(0, 0)])
print(f"Total paths found: {ans}")
