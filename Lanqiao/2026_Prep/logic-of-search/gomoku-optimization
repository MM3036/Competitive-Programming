# 全局变量
board = [0] * 25  # 一维数组模拟 5x5 棋盘
ans = 0           # 记录平局数量

# 辅助函数：快速检查刚才落下的子是否导致了连珠
# 只要检查经过 idx 的行、列、对角线即可
def check_is_win(idx, color):
    r, c = idx // 5, idx % 5
    
    # 1. 检查行
    # 这一行的起点是 r * 5
    row_start = r * 5
    if all(board[row_start + i] == color for i in range(5)):
        return True
        
    # 2. 检查列
    # 这一列的起点是 c, 每次 +5
    if all(board[c + i*5] == color for i in range(5)):
        return True
        
    # 3. 检查主对角线 (只有当 idx 在对角线上时才查)
    # 主对角线上的点满足 r == c (0, 6, 12, 18, 24)
    if r == c:
        if all(board[i*6] == color for i in range(5)):
            return True

    # 4. 检查副对角线
    # 副对角线上的点满足 r + c == 4 (4, 8, 12, 16, 20)
    if r + c == 4:
        if all(board[4 + i*4] == color for i in range(5)):
            return True
            
    return False

def dfs(idx, white_cnt, black_cnt):
    global ans
    
    # --- 1. 终局判断 (Base Case) ---
    if idx == 25:
        # 能走到这里，说明中间没有任何人赢，且棋盘填满了
        ans += 1
        return

    # --- 2. 剪枝前置 (Pruning) ---
    # 如果剩余的格子不够填满白棋或黑棋，直接放弃
    remaining_cells = 25 - idx
    if remaining_cells < (13 - white_cnt) or remaining_cells < (12 - black_cnt):
        return

    # --- 3. 递归与回溯 (The Loop) ---
    
    # 【选项 A：尝试放白棋】
    if white_cnt < 13:
        board[idx] = 1 # 落子
        # 关键逻辑：只有当“这一步没赢”时，才允许继续往下走
        # 如果这一步赢了，就不递归了（剪枝），因为我们要的是平局
        if not check_is_win(idx, 1):
            dfs(idx + 1, white_cnt + 1, black_cnt)
        board[idx] = 0 # 【回溯：打扫现场，消灭幽灵棋子】

    # 【选项 B：尝试放黑棋】
    if black_cnt < 12:
        board[idx] = 2 # 落子
        if not check_is_win(idx, 2):
            dfs(idx + 1, white_cnt, black_cnt + 1)
        board[idx] = 0 # 【回溯：打扫现场】

# --- 主程序 ---
# 小蓝（白棋）先手，需要下 13 个
# 小桥（黑棋）后手，需要下 12 个
print("正在计算中，请稍候... (大约需要几秒钟)")
dfs(0, 0, 0)
print(f"满足条件的平局总数是: {ans}")
