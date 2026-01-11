import sys
from collections import defaultdict
#导入快速读取需要的库和默认字典
try:
    #防御式编程
    data = map(int, sys.stdin.read().split())
    #全部吞下再返回迭代器一个一个吐，即节省时间（读数据）又节省空间（迭代器
    #至于在调用时才会生成数据占用空间）
    n = next(data)
    m = next(data)
    #迭代器一口全下去后前两个就是n和m
    main_cnt = defaultdict(int)
    anti_cnt = defaultdict(int)
    #用defaultdict生成字典更加方便无需讨论是否字典中已经存在目标值
    ans = 0
    for r in range(n):
        for c in range(m):
            #如果不需要坐标只需要每个值绝对不用双层for循环，若需要则写range
            #底层是C++很快
            val = next(data)
            key_main = (r - c, val)
            #通过元组唯一标识数据
            ans += main_cnt[key_main]
            #贡献法，在线处理，计算机的处理方式，不去处理总体，只算增量，启动快
            main_cnt[key_main] += 1
            #将新来的数据加入已有数据中，下面同理：
            key_anti = (r + c, val)
            ans += anti_cnt[key_anti]
            anti_cnt[key_anti] += 1
    print(ans)
except stopIteration:
    pass
