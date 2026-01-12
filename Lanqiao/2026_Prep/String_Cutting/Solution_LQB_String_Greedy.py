import sys
s = input()
#只有一行输入，input输入
li = ["lqb", "lbq", "blq", "bql", "qlb", "qbl"]
#通过集合哈希存储，变查找为计算，时间复杂度O（1）
ans = 0
i = 0
while i + 3 <= len(s):
    ss = s[i:i+3]
    if ss in li:
        ans += 1
        i += 3
        #题目说的切割，所以符合标准的不能二次利用
    else:
        i += 1
print(ans)
