import sys

# 使用读取所有输入并去掉首尾空白字符，应对大数据量更稳健
s = sys.stdin.read().strip()

# 使用集合（Set）实现哈希存储，查找复杂度为 O(1)
target_set = {"lqb", "lbq", "blq", "bql", "qlb", "qbl"}

ans = 0
i = 0
n = len(s)

while i + 3 <= n:
    # 这里的切片操作是 O(k)，k=3，总体复杂度 O(n)
    if s[i:i+3] in target_set:
        ans += 1
        i += 3  # 匹配成功，跳过这3个字符（切割）
    else:
        i += 1  # 匹配失败，向后移动一位
        
print(ans)
