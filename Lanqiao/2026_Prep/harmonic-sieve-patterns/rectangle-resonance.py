L = int(input())
MOD = 10 ** 9 + 7  
# Python里写 1e9+7 得到的是浮点数，要用整数写法
energy = [0] * (L + 1)
for w in range(1, L + 1):
    for area in range(w, L + 1, w):
        h = area // w  
        weight = w + h 
        energy[area] += weight
# 筛法预处理 (Sieve)算出每个面积 area 对应的所有矩形半周长之和
prefix_E = [0] * (L + 1)
for i in range(1, L + 1):
        #一边加一边取模，防止数字过大（虽然Python不怕大数，但取模快一点）
    prefix_E[i] = (prefix_E[i - 1] + energy[i]) % MOD
# 第二步：前缀和,为了快速算出 1 到 k 范围内所有 energy 的和
ans = 0
for u in range(1, L + 1):
        # 根据 u * v <= L，算出 v 的最大值
    max_v = L // u
        # 既然 v 可以取 1 到 max_v 的任意值
        # 那么 v 的所有能量之和就是 prefix_E[max_v]
    sum_v_energy = prefix_E[max_v]
    term = (energy[u] * sum_v_energy) % MOD
    ans = (ans + term) % MOD
# 第三步：统计答案 u * v <= L，利用除法消灭内层循环
print(ans)
