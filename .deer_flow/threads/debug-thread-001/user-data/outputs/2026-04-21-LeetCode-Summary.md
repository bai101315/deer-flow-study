# 2026-04-21 LeetCode 刷题总结

## 概述

今日是 2026 年 4 月 21 日，星期二。完成了 **9 道不同题目**，共 **22 次提交**（包含重复提交优化），再次超越每日 6 题的目标。今日完成了每日挑战 **1722. 执行交换操作后的最小汉明距离**，同时深入练习了数组、前缀和、滑动窗口、DFS/BFS 等核心算法技巧。

---

## 当天统计

| 难度等级 | 数量 | 占比 |
|----------|------|------|
| Medium   | 8    | 88.9% |
| Hard     | 1    | 11.1% |

**主要知识点分布**：数组操作、双指针、滑动窗口、哈希表、前缀和、DFS/BFS、贪心、动态规划入门、矩阵操作

---

## 题目总结

### 1. 交换元素后的最大交替和

**难度**: Medium | **知识点**: 贪心、数组

**难点分析**:
- 需要理解交替和的定义：奇数位置元素之和减去偶数位置元素之和
- 交换操作的本质是将较大值交换到奇数位置，较交换到偶数位置
- 通过排序和贪心策略找到最优交换对

**解题代码**:
```python
def maximumAlternatingSum(nums):
    # 贪心：将最大奇数位置安排最大元素，最小偶数位置安排最小元素
    # 简化：只关心能否通过交换提升交替和
    # 实际需要考虑交换成本和收益
    pass  # 详细解法略
```

---

### 2. 交换字符串中的元素

**难度**: Medium | **知识点**: 并查集、哈希表、字符串

**难点分析**:
- 需要理解「可交换」关系的传递性（并查集）
- 同一连通分量内的字符可以任意排列
- 先对每个位置找到其所属的连通分量，再对连通分量内字符排序

**解题代码**:
```python
def smallestStringWithSwaps(s, pairs):
    parent = list(range(len(s)))
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
    
    for a, b in pairs:
        union(a, b)
    
    # 分组并排序
    groups = defaultdict(list)
    for i in range(len(s)):
        groups[find(i)].append(s[i])
    
    for key in groups:
        groups[key].sort()
    
    # 重建字符串
    result = []
    for i in range(len(s)):
        key = find(i)
        result.append(groups[key].pop(0))
    
    return ''.join(result)
```

---

### 3. 执行交换操作后的最小汉明距离

**难度**: Medium | **知识点**: 并查集、哈希表

**难点分析**:
- 理解汉明距离：相同位置不同字符的计数
- 利用交换操作可以调整源数组的元素位置
- 通过并查集判断哪些位置可以通过交换达到目标位置

**解题代码**:
```python
def minimumHammingDistance(source, target, allowedSwaps):
    n = len(source)
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
    
    for a, b in allowedSwaps:
        union(a, b)
    
    # 统计每个连通分量内的元素差异
    from collections import Counter
    diff = 0
    groups = defaultdict(Counter)
    
    for i in range(n):
        groups[find(i)][source[i]] += 1
    
    for i in range(n):
        key = find(i)
        if groups[key][target[i]] > 0:
            groups[key][target[i]] -= 1
        else:
            diff += 1
    
    return diff
```

---

### 4. 矩阵置零

**难度**: Medium | **知识点**: 数组、矩阵

**难点分析**:
- 原地修改矩阵，不能使用额外空间（常数空间）
- 需要记录哪些行和列需要置零
- 利用矩阵第一行和第一列作为标记

**解题代码**:
```python
def setZeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))
    
    # 用第一行和第一列标记
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    
    # 根据标记置零
    for i in range(1, m):
        if matrix[i][0] == 0:
            for j in range(n):
                matrix[i][j] = 0
    
    for j in range(1, n):
        if matrix[0][j] == 0:
            for i in range(m):
                matrix[i][j] = 0
    
    # 处理第一行和第一列
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0
```

---

### 5. 除了自身以外数组的乘积

**难度**: Medium | **知识点**: 前缀积、数组

**难点分析**:
- 不能使用除法
- 需要构建左右两个方向的乘积数组
- 优化：使用 O(1) 额外空间

**解题代码**:
```python
def productExceptSelf(nums):
    n = len(nums)
    result = [1] * n
    
    # 计算左侧乘积
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    
    # 计算右侧乘积并合并
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    
    return result
```

---

### 6. 合并区间

**难度**: Medium | **知识点**: 排序、区间合并

**难点分析**:
- 先按左端点排序
- 依次合并有重叠的区间
- 经典贪心解法

**解题代码**:
```python
def merge(intervals):
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    result = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    
    return result
```

---

### 7. 最大子数组和

**难度**: Medium | **知识点**: 动态规划、贪心、Kadane 算法

**难点分析**:
- 理解「连续子数组」的概念
- Kadane 算法核心：当前和为负数时重新开始

**解题代码**:
```python
def maxSubArray(nums):
    max_sum = nums[0]
    current_sum = nums[0]
    
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

---

### 8. 绝对差不超过限制的最长连续子数组

**难度**: Medium | **知识点**: 滑动窗口、有序数据结构

**难点分析**:
- 需要快速获取窗口内最大值和最小值
- 使用单调队列或平衡树（SortedList）
- 双指针维护滑动窗口

**解题代码**:
```python
def longestSubarray(nums, limit):
    from collections import deque
    
    max_q = deque()  # 单调递减队列
    min_q = deque()  # 单调递增队列
    left = 0
    result = 0
    
    for right in range(len(nums)):
        # 维护最大值队列
        while max_q and nums[right] > max_q[-1]:
            max_q.pop()
        max_q.append(nums[right])
        
        # 维护最小值队列
        while min_q and nums[right] < min_q[-1]:
            min_q.pop()
        min_q.append(nums[right])
        
        # 收缩窗口
        while max_q[0] - min_q[0] > limit:
            if nums[left] == max_q[0]:
                max_q.popleft()
            if nums[left] == min_q[0]:
                min_q.popleft()
            left += 1
        
        result = max(result, right - left + 1)
    
    return result
```

---

### 9. 滑动窗口最大值

**难度**: Hard | **知识点**: 单调队列、滑动窗口

**难点分析**:
- 需要 O(n) 时间复杂度
- 使用单调递减队列维护窗口内最大值
- 队列存储索引而非值

**解题代码**:
```python
def maxSlidingWindow(nums, k):
    from collections import deque
    
    q = deque()  # 存储索引，保持单调递减
    result = []
    
    for i, num in enumerate(nums):
        # 移除超出窗口的索引
        while q and q[0] <= i - k:
            q.popleft()
        
        # 保持单调递减
        while q and nums[q[-1]] <= num:
            q.pop()
        
        q.append(i)
        
        # 记录结果
        if i >= k - 1:
            result.append(nums[q[0]])
    
    return result
```

---

## 总体总结

### 当天重点

1. **并查集的深度理解**：今日多次用到并查集处理「可交换」关系，包括交换字符串、最小汉明距离等题目
2. **滑动窗口技巧**：通过单调队列实现 O(n) 时间复杂度的最大值/最小值查询
3. **数组空间优化**：除了自身以外数组的乘积展示了如何在 O(1) 空间内完成复杂操作

### 学习收获

- 并查集是处理「关系传递性」问题的利器，特别是在涉及位置交换的场景
- 单调队列是滑动窗口类问题的核心优化手段
- 前缀积/前缀和思想可以解决很多「排除特定元素」的问题
- 原地修改矩阵需要巧用标记行/列

### 改进方向

1. **复杂并查集应用**：部分题目在合并后元素分配时还有优化空间
2. **边界条件处理**：注意空数组、单元素数组的边界情况
3. **代码鲁棒性**：加强错误输入的容错处理

### 明日计划

1. 继续巩固并查集相关题目
2. 深入练习单调栈/单调队列高级应用
3. 尝试 Hard 级别题目，挑战舒适区
4. 保持每日刷题节奏，争取稳定在 8+ 题目

---

*总结日期: 2026-04-21*
*总通过题目: 9*
*主要知识点: 并查集、滑动窗口、单调队列、前缀和、贪心、DFS/BFS、矩阵操作*