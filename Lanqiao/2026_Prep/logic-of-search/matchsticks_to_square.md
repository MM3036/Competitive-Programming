# [算法笔记] DFS 回溯与强力剪枝：
*火柴拼正方形题目代号：防线重建 / LeetCode 473. Matchsticks to Square*
*核心考察：DFS 回溯 (Backtracking)、集合划分、剪枝优化 (Pruning)*
## 1. 题目简述
  给定一个整数数组 matchsticks，代表火柴棒的长度。要求判断能否将所有火柴棒
  拼成一个正方形（即拼成 4 条边，每条边长度相等，且必须用完所有火柴）。
## 2. 核心思路：
  ## 1. 题目简述
给定一个整数数组 `matchsticks`，代表火柴棒的长度。要求判断能否将所有火柴棒拼成一个正方形（即拼成 4 条边，每条边长度相等，且必须用完所有火柴）。

## 2. 核心思路
从暴力到优化，这道题本质上是一个 **“分组问题”**：把 $N$ 个物品分成 4 组，每组的和必须等于 `总和 / 4`。

### 2.1 基础架构：DFS + 回溯
我们定义一个递归函数，尝试填充这 4 条边。
* **状态定义**：当前填到了第几条边？当前这条边填了多长？从哪根火柴开始找？
* **回溯本质**：做选择（标记已用） -> 递归（下探） -> 撤销选择（恢复现场）。

### 2.2 我的踩坑历程（Debug 复盘）
在初次实现时，我犯了几个典型的错误，值得记录：

1.  **数学误区**：误以为边长是 `avg = sum // len`，实际应为 `sum // 4`。
2.  **缺少回溯**：在递归返回后，忘记将 `visited[i]` 重置为 `False`，导致状态污染。
3.  **返回传递失效**：即“传声筒”机制失效。下层递归找到了 `True`，但上层没有通过 `if dfs(): return True` 将结果向上传递，导致程序继续空转。

## 3. 关键剪枝策略（Pruning）—— 如何由慢变快？
如果不剪枝，复杂度是指数级 $O(4^N)$，数据稍大即超时。本题有三个 **“必杀技”** 级别的剪枝：

### 3.1 排序剪枝 (Sorting)
* **策略**：`nums.sort(reverse=True)`
* **原理**：先处理大的，再处理小的。如果一根很长的火柴（大岩石）无法放入当前的桶，那么整个方案直接失败。如果先处理沙子（小火柴），可能递归很深才发现大岩石放不下，浪费计算资源。

### 3.2 对称性剪枝 (Symmetry / val == 0)
**代码：**
```python
if val == 0: return False
```
**逻辑**：
如果在一条全新的空边（`val == 0`）尝试放入某根火柴导致了最终失败，那么就不需要把这根火柴拿到第 2、3、4 条空边去试了。因为 4 条空边在数学上是 **完全等价的**。在这里失败，在那里也一定失败。直接判定当前分支无解。

### 3.3 贪心/交换论证剪枝 (val + li[i] == target)
**代码：**
```python
if val + li[i] == target: return False
```
**逻辑**：
如果当前这根火柴刚好能填满这一条边（完美匹配），但递归下去发现后续无法完成。此时 **不要尝试用几根小火柴来代替这根大火柴填坑！**

> **原因**：在拼凑问题中，保留“大块完整”的资源给后面，通常比保留“细碎”的资源更难处理。如果不使用“完美匹配”都导致失败，那么拆东墙补西墙（用碎的凑）更不可能成功。

## 4. 最终代码实现 (Python)
这是基于 **“DFS 万能模板”** 修正后的最终版本。

```python
# 增加递归深度，防止爆栈
sys.setrecursionlimit(2000)

class Solution:
    def makesquare(self, matchsticks: list[int]) -> bool:
        total_len = sum(matchsticks)
        # 剪枝 0：基本数学检查
        if total_len % 4 != 0:
            return False
            
        target = total_len // 4
        
        # 剪枝 1：从大到小排序 (关键！)
        matchsticks.sort(reverse=True)
        
        # 状态数组：记录火柴是否被使用
        mem = [False] * len(matchsticks)
        
        # dfs(已完成边数, 当前边长度, 搜索起点)
        def dfs(edges_done, current_len, start_index):
            # 1. 终点检查：如果拼好了3条边，第4条自然也就好了
            if edges_done == 3:
                return True
            
            # 2. 换边逻辑：如果当前边拼满了
            if current_len == target:
                # 开启下一条边 (edges_done + 1)，长度清零，搜索起点重置为 0
                return dfs(edges_done + 1, 0, 0)
            
            # 3. 遍历选择
            for i in range(start_index, len(matchsticks)):
                if not mem[i]:
                    # 剪枝：如果加上这就超长了，跳过
                    if current_len + matchsticks[i] > target:
                        continue
                    
                    # 4. 做选择
                    mem[i] = True
                    
                    # 5. 【传声筒】下探递归
                    # 注意：如果当前没满，继续填当前边，只能往后找 (i+1)
                    if dfs(edges_done, current_len + matchsticks[i], i + 1):
                        return True
                    
                    # 6. 撤销选择 (回溯)
                    mem[i] = False
                    
                    # 7. 【强力剪枝】 (逻辑推导核心)
                    # 如果刚才那根火柴失败了，且满足以下任一条件，直接判死刑：
                    # a) 它是空边的第一根 (val == 0) -> 对称性剪枝
                    # b) 它刚好填满当前边 (val + item == target) -> 贪心剪枝
                    if current_len == 0 or current_len + matchsticks[i] == target:
                        return False
                        
            # 所有路都试完了都不行
            return False

        return dfs(0, 0, 0)

# 本地测试部分
if __name__ == "__main__":
    sol = Solution()
    # 示例
    print(sol.makesquare([1, 1, 2, 2, 2])) # Expect: True
    print(sol.makesquare([3, 3, 3, 3, 4])) # Expect: False
```

## 5. 心得与总结DFS 的本质：
就是**“结束条件 + 递归下探 + 回溯还原”**。它本质是暴力枚举，但结构很固定。
关于“传声筒”：递归函数中，如果下层返回 True，上层必须立刻 return True，否则结果会丢失。
计算不是万能的，逻辑才是：计算机算得再快，也怕指数级爆炸。通过数据的性质（如对称性、贪心策略）
进行逻辑推理，从而跳过大量无效计算，这才是算法的魅力。
做题心态：不要反感背模板。模板是抓住了**“变中之不变”**。把骨架内化成肌肉记忆，才能腾出脑力去思考每一道题特有的剪枝逻辑。
