L = int(input())
div_num = [0] * (L + 1)
#因为从一开始，所以0是空着的，加一其实不用只是绝对安全
for factor in range(1, L):
    for i in range(i, L, i):
        div_num[i] += 1
#筛法、贡献思想，不再枚举每个数的约数，转为找产生了那些因数
prefix_sum_div = [0] * (L + 1)
for j in range(1, L):
    prefix_sum_div[j] = prefix_sum_div[j - 1] + div_num[j]
#前缀和，当前答案借助上一个答案生成并存储下来，用空间换时间
ans = 0
for u in range(1, L):
    v = L - u
    ans += div_num[u] * prefix_sum_div[v]
