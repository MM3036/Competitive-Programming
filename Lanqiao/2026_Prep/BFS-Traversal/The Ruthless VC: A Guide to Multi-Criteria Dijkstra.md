# 算法笔记：紧急救援 (The Emergency Rescue) —— 多维权值 Dijkstra 的深度解析

## 1. 题目概要 (Problem Definition)

**背景设定**：
在一个包含 $N$ 个城市和 $M$ 条双向道路的图中，需要寻找从起点 $S$ 到终点 $D$ 的最优路径。

**数据结构属性**：
*   **边权 (Edge Weight)**：道路通行时间（代价函数 $C$，求最小化）。
*   **点权 (Node Weight)**：城市救援人员数量（收益函数 $W$，求最大化）。

**核心目标 (Dual Objectives)**：
1.  **第一优先级**：找到时间最短的路径。
2.  **第二优先级**：若时间相同，选择沿途召集救援人员总数最多的路径。

---

## 2. 常见误区分析 (Fail Fast & Learn)

### 🔴 误区 A：优先队列的“引力方向”错误
*   **错误直觉**：想求“人数最多”，于是把正的人数直接扔进堆里。
*   **物理真相**：`heapq` 是**小顶堆**，受重力影响，只喜欢“小”的数字。存正数会导致优先弹出人数最少的路。
*   **修正 (The Trick)**：**存负数**！存 `(cost, -people, u)`。Python 选最小的负数（如 -100 < -5），逻辑上即是在选最大的人数（100 > 5）。

### 🔴 误区 B：内存污染 (Memory Corruption)
*   **错误想法**：直接修改输入的 `nums` 数组做累加。
*   **物理真相**：地图数据应视为**只读 (Read-Only)**。若直接修改，当另一条路经过该点时，会读到错误的数据，导致数值“通货膨胀”。
*   **修正**：开辟独立的 `max_people` 数组作为记分牌（读写）。

### 🔴 误区 C：拿了芝麻丢了西瓜
*   **错误想法**：`if new_dist < dist[v]` 更新距离时，忘了更新人数。
*   **物理真相**：**时间是绝对主宰**。当发现更快的路时，旧路上积累的人数（哪怕再多）也必须作废。
*   **修正**：距离被优化的瞬间，强制覆盖人数和前驱节点。

---

## 3. 核心思维模型 (The Mental Models)

### 💡 1. 资本家模型 (The Capitalist VC)
**Dijkstra 算法不是邮差，而是一个精明且冷酷的风投家。**

*   **算力 = 资金**。它永远只把资金投给当前回报率最高（代价最小）的项目。
*   **倾斜机制**：只要快的那条路（代价低），资本就会一直推着它走。一旦它遇到高山（代价飙升），资本立刻撤资，转头去推那个原本慢吞吞但现在看来更便宜的“备胎”。

### 💡 2. 嫁接理论 (The Grafting)
**关于“乱改路径”的终极解释。**

*   **疑问**：B 方案后来居上，修改了 A 方案的 parents，会不会导致路径错乱？
*   **顿悟**：不会。这种“篡改”实际上是**优化**。
    *   我们将后续所有的路径从 A 这个“烂树干”上砍下来。
    *   **嫁接**到了 B 这个“好树干”上。
    *   整棵树因此变得更短、更强。我们不需要保留旧的 A，因为我们只要最优解。

### 💡 3. 双重松弛逻辑 (Dual Relaxation)
代码落地的核心在于处理两种不同的“松弛”情况：

*   **Case 1：颠覆 (Dominance)**
    `if new_dist < dist[v]`：发现新大陆。时间缩短，**无条件**更新距离、更新人数、更新父亲。
*   **Case 2：改良 (Pareto Improvement)**
    `elif new_dist == dist[v]`：发现平行宇宙。时间一样，**比较人数**。如果 `new_people > max_people[v]`，则更新人数和父亲。

---

## 4. 路径还原 (Path Reconstruction)

*   **反向存储**：`parents` 存的是“谁是我的爸爸”。找爸爸是唯一的，找儿子会分叉。
*   **防爆短路**：`if path and path[-1] == S`。防止在终点不可达（path为空或断裂）时报错。
*   **死循环锁**：`if curr == S: break`。防止逻辑 Bug 导致无限转圈。

---

## 5. 标准答案 (Standard Solution)

```python
import sys
import collections
import heapq

# 读取所有输入
data = map(int, sys.stdin.read().split())
iterator = iter(data) # 变成流

try:
    N = next(iterator)
    M = next(iterator)
    S = next(iterator)
    D = next(iterator)
    
    # [Fix 1]: 先开辟空间，不要让 list 越界
    # 既然 N 是总数，我们通常需要 0 到 N-1，或者 1 到 N
    # 题目如果没说是 1-based，通常假设 0-based 比较安全，或者开大一点
    nums = [0] * (N + 1)
    
    # 你的循环逻辑有点乱，通常题目会给出 N 个数
    for i in range(N): 
        # 假设题目给的是 0~N-1 号城市的人数
        # 如果是 1~N，这里要根据题目调整
        nums[i] = next(iterator) 

    # [Fix 2]: 必须传 list 类，不是 []
    graph = collections.defaultdict(list)
    for _ in range(M):
        u = next(iterator)
        v = next(iterator)
        w = next(iterator)
        graph[u].append((v, w))
        graph[v].append((u, w))

except StopIteration:
    sys.exit(0)

# parent 放在外面或者里面都可以，建议放里面或者传参
def dijkstra(n, start, end, graph, people_per_city):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    
    # max_people[i] 记录到达 i 的最大集结人数
    max_people = [0] * (n + 1)
    max_people[start] = people_per_city[start]
    
    parents = [None] * (n + 1)
    
    pq = []
    # [Fix 3]: 存负数 (-people) 来实现最大堆效果
    heapq.heappush(pq, (0, -people_per_city[start], start))
    
    while pq:
        d, neg_people, u = heapq.heappop(pq)
        current_people = -neg_people # 取出来变回正数
        
        # [Fail Fast]: 距离更大，或者 距离相等但人数更少，都跳过
        if d > dist[u]:
            continue
        if d == dist[u] and current_people < max_people[u]:
            continue
            
        # [Fix 4]: 必须遍历 graph[u]
        for v, w in graph[u]:
            new_dist = d + w
            new_total_people = current_people + people_per_city[v]
            
            # 情况 A: 发现更短路
            if new_dist < dist[v]:
                dist[v] = new_dist
                # [Fix 5]: 必须同步更新人数！
                max_people[v] = new_total_people
                parents[v] = u
                heapq.heappush(pq, (new_dist, -new_total_people, v))
            
            # 情况 B: 距离一样，人更多
            elif new_dist == dist[v]:
                if new_total_people > max_people[v]:
                    max_people[v] = new_total_people
                    parents[v] = u
                    # 只要状态更新了（哪怕只有人数），也要入队传播
                    heapq.heappush(pq, (new_dist, -new_total_people, v))
                    
    return dist, max_people, parents

# 执行
final_dist, final_people, parents = dijkstra(N, S, D, graph, nums)

# 输出逻辑
if final_dist[D] == float('inf'):
    print(-1)
else:
    print(f"{final_dist[D]} {final_people[D]}")
    
    # 路径还原
    path = []
    curr = D
    while curr is not None:
        path.append(curr)
        if curr == S: break # 防止死循环
        curr = parents[curr]
    
    # 补丁：如果没找到路径（比如不可达），path可能只有D一个点且不可达
    # 简单判断：如果 path 最后一个不是 S，说明断了
    if path and path[-1] == S:
        print("->".join(map(str, path[::-1])))
```

## 6. 总结 (Summary)

本题是 **Dijkstra 算法** 在多维约束下的经典应用。解决此类问题的关键在于：

1.  **优先级明确**：必须严格遵循“先比较第一权值（距离），再比较第二权值（点权）”的原则，不可混淆。
2.  **数据结构适配**：利用 `(dist, -weight, node)` 的元组结构巧妙适配 Python 的最小堆特性。
3.  **状态管理的独立性**：将“地图数据”与“状态数据”分离，避免计算过程中的数据污染。
4.  **理解松弛本质**：松弛操作（Relaxation）本质上是路径树的**动态修剪与嫁接**，这一物理视角的理解比死记代码更重要。
