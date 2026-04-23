# 2026-04-20 LeetCode 刷题总结

## 概述

今日是2026年4月20日（周一），继续进行LeetCode刷题训练。通过leetcode_get_user_status验证已登录后，使用leetcode_get_all_submissions工具获取今日的完整提交记录。

今日完成5道AC题目，难度分布为Easy×2、Medium×2、Hard×1，相比昨日10题的记录有所减少，但仍保持稳定的练习节奏。

## 当天统计

| 难度等级 | 数量 | 占比 |
|---------|------|------|
| Easy    | 2    | 40%  |
| Medium  | 2    | 40%  |
| Hard    | 1    | 20%  |

**主要知识点分布**：数学、动态规划、数组、双指针、BFS、贪心、前缀和、哈希表、滑动窗口

---

## 题目总结

### 1. 统计特殊整数 (Count Special Integers)

**难度**: Hard | **知识点**: 数学、动态规划

**难点分析**:
- 需要计算1到n之间所有数字位数都不同的特殊整数
- 使用数位DP（Digit DP）结合位掩码来记录已使用的数字
- 需要处理前导零的情况
- 对不同位数的数字分别统计

**解题代码**:
```python
class Solution:
    def countSpecialNumbers(self, n: int) -> int:
        s = str(n)
        m = len(s)
        
        @lru_cache(None)
        def f(pos: int, tight: bool, started: bool, mask: int) -> int:
            if pos == m:
                return 1 if started else 0
            limit = int(s[pos]) if tight else 9
            res = 0
            for d in range(limit + 1):
                nstarted = started or (d != 0)
                nmask = mask
                if nstarted:
                    if mask & (1 << d):
                        continue
                    nmask = mask | (1 << d)
                res += f(pos + 1, tight and d == limit, nstarted, nmask)
            if not started:
                res += 1  # Leading zeros (shorter numbers)
            return res
        
        return f(0, True, False, 0)
```

---

### 2. 两栋颜色不同且距离最远的房子 (Two Furthest Houses With Different Colors)

**难度**: Easy | **知识点**: 贪心、数组

**难点分析**:
- 给定颜色的数组，寻找颜色不同的两栋房子之间的最大距离
- 贪心策略：最大距离必然来自最左边或最右边的房子与另一侧某栋不同颜色房子的配对
- O(n)时间复杂度即可解决

**解题代码**:
```python
class Solution:
    def maxDistance(self, colors: List[int]) -> int:
        n = len(colors)
        left = 0
        while left < n - 1 and colors[left] == colors[n-1]:
            left += 1
        right = n - 1
        while right > 0 and colors[right] == colors[0]:
            right -= 1
        return max(n - 1 - left, right)
```

---

### 3. 多源图像渲染 (Multi Source Flood Fill)

**难度**: Medium | **知识点**: BFS

**难点分析**:
- 多个源点同时从四个方向扩散填充颜色
- 同一格子被多个颜色同时到达时，取数值最大的颜色
- 使用多源BFS，按层扩散
- 需要记录每个格子的到达时间以处理冲突

**解题代码**:
```python
class Solution:
    def colorGrid(self, n: int, m: int, sources: List[List[int]]) -> List[List[int]]:
        grid = [[0] * m for _ in range(n)]
        dist = [[-1] * m for _ in range(n)]
        q = deque()
        for r, c, color in sources:
            grid[r][c] = color
            dist[r][c] = 0
            q.append((r, c, color))
        
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        while q:
            r, c, color = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    grid[nr][nc] = color
                    q.append((nr, nc, color))
                elif 0 <= nr < n and 0 <= nc < m and dist[nr][nc] == dist[r][c] + 1:
                    grid[nr][nc] = max(grid[nr][nc], color)
        return grid
```

---

### 4. 最小稳定下标 II (Smallest Stable Index II)

**难度**: Medium | **知识点**: 前缀最大值、后缀最小值

**难点分析**:
- 稳定性得分定义为 max(nums[0..i]) - min(nums[i..n-1])
- 需要找到第一个稳定性得分 ≤ k 的下标
- 分别预计算前缀最大值数组和后缀最小值数组
- 遍历检查每个下标即可

**解题代码**:
```python
class Solution:
    def firstStableIndex(self, nums: List[int], k: int) -> int:
        n = len(nums)
        pref_max = [0] * n
        suff_min = [0] * n
        
        pref_max[0] = nums[0]
        for i in range(1, n):
            pref_max[i] = max(pref_max[i-1], nums[i])
        
        suff_min[n-1] = nums[n-1]
        for i in range(n-2, -1, -1):
            suff_min[i] = min(suff_min[i+1], nums[i])
        
        for i in range(n):
            if pref_max[i] - suff_min[i] <= k:
                return i
        return -1
```

---

### 5. 最小稳定下标 I (Smallest Stable Index I)

**难度**: Easy | **知识点**: 数组、模拟

**难点分析**:
- 简化版的稳定性下标问题，数据规模较小
- 直接模拟计算每个位置的稳定性得分即可
- O(n²) 在小规模数据下可接受

**解题代码**:
```python
class Solution:
    def firstStableIndex(self, nums: List[int], k: int) -> int:
        n = len(nums)
        for i in range(n):
            left_max = max(nums[:i+1])
            right_min = min(nums[i:])
            if left_max - right_min <= k:
                return i
        return -1
```

---

## 总体总结

### 当天重点

1. **掌握了数位DP（Digit DP）的应用**：统计特殊整数问题需要结合数位DP和位掩码处理，是Hard级别的数学动态规划问题
2. **多源BFS算法**：多源图像渲染问题复习了多源广度优先搜索的应用场景
3. **前缀/后缀预计算技巧**：最小稳定下标问题展示了预计算前缀最大值和后缀最小值的经典方法

### 学习收获

- 巩固了数位DP的模板写法，特别是处理前导零和tight约束的技巧
- 学会了将复杂问题分解为预处理数组+单次遍历的优化思路
- 复习了多源BFS在图论问题中的应用

### 改进方向

- 继续加大Hard题目的练习力度，提升数学思维和DP能力
- 对于_medium_级别的题目，可以尝试多种解法比较优劣
- 保持每日的刷题节奏，争取稳定在每日6题以上

### 明日计划

1. 继续巩固数位DP相关题目
2. 挑战更多Hard级别题目
3. 复习前缀和、哈希表相关的中等题目
4. 保持每日的提交记录和总结

---

*总结日期: 2026-04-20*  
*总通过题目: ~90+*  
*主要知识点: 数学、动态规划、BFS、双指针、前缀和、哈希表*