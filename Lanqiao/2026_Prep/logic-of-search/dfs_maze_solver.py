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
这道题我要上传github帮我起个文件名还有标题描述，英文
