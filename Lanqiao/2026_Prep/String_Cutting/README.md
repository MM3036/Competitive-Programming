# 蓝桥杯 Python 算法笔记：字符串匹配优化与贪心思想

## 1. 查找性能优化：哈希 (Hashing) vs 列表
在进行频繁的 `in` 操作判断子串是否存在时，数据结构的选择至关重要。

* **问题**：原代码使用列表 `li` (`["lqb", "lbq", ...]`) 存储匹配项。在 Python 中，列表的 `in` 操作通常需要遍历，时间复杂度为 **O(n)**。
* **优化**：应使用 **集合 (Set)**。
    ```python
    # 优化前
    li = ["lqb", "lbq", "blq", "bql", "qlb", "qbl"]
    
    # 优化后：查找时间复杂度降为 O(1)
    li = {"lqb", "lbq", "blq", "bql", "qlb", "qbl"} 
    ```
    > **Highlight**: 在算法竞赛中，当需要大量查询“是否存在”时，优先选择哈希表（Set 或 Dict）。

## 2. 输入处理技巧
对于 Python 竞赛编程，处理单行字符串输入非常简洁：

```python
# 不需要 sys.stdin.readline().strip() 时的简单写法
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

