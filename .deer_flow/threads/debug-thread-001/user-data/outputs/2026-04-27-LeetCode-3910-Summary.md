# 2026-04-27 LeetCode 刷题总结

## 概述

今日挑战 LeetCode 第 3910 题 **Count Connected Subgraphs with Even Node Sum**（统计节点和为偶数的连通子图），一道 Hard 难度的图论+位运算综合题。成功通过全部 954 个测试用例，获得 Accepted。

## 当天统计

| 难度等级 | 数量 | 占比 |
|----------|------|------|
| Hard     | 1    | 100% |

**主要知识点分布**：图论、位运算、深度优先搜索（DFS）、子集枚举、连通性判断

---

## 题目总结

### 1. Count Connected Subgraphs with Even Node Sum

**难度**: Hard | **知识点**: 图论、位运算、DFS、子集枚举

**难点分析**:

- **难点1：暴力枚举的复杂度控制**
  - 核心点：n ≤ 13，最多 2^13 - 1 = 8191 个非空子集，可采用位掩码（bitmask）枚举所有子集
  - 解决方法：使用 `for sub in range(1, (1 << n))` 枚举所有子集，用 `sub >> i & 1` 判断节点 i 是否被选中

- **难点2：偶数和的高效判断**
  - 核心点：由于 nums[i] ∈ {0, 1}，求和可简化为异或操作：若子集中 1 的个数为偶数，则和为偶数
  - 解决方法：用 `xor_sum ^= nums[i]` 累计奇偶性，避免重复求和

- **难点3：连通性的高效验证**
  - 核心点：对每个子集，需要判断其诱导子图是否连通。可从子集中任一节点出发做 DFS/BFS，检查是否能访问到子集中所有节点
  - 解决方法：选取子集的最高位节点作为 DFS 起点，用 `vis` 位掩码记录已访问节点，遍历结束后判断 `vis == sub`（所有子集节点均被访问）

**解题代码**:

```python
class Solution:
    def evenSumSubgraphs(self, nums: list[int], edges: list[list[int]]) -> int:
        # 构建邻接表
        n = len(nums)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        u = (1 << n) - 1
        res = 0
        
        # 枚举所有非空子集
        for sub in range(1, u + 1):
            # 检查节点值之和是否为偶数（使用异或判断奇偶性）
            xor_sum = 0
            for i, x in enumerate(nums):
                if sub >> i & 1:
                    xor_sum ^= x
            
            # 奇数和，跳过
            if xor_sum:
                continue
            
            # 检查连通性：从子集中任意节点出发 DFS
            vis = 0  # 已访问节点位掩码
            
            def dfs(x):
                nonlocal vis
                vis |= (1 << x)
                for y in g[x]:
                    if not (vis >> y) & 1:
                        dfs(y)
            
            # 选取子集中编号最大的节点作为起点（bit_length - 1）
            start = sub.bit_length() - 1
            dfs(start)
            
            # 若访问了所有子集中的节点，则连通
            if vis == sub:
                res += 1

        return res
```

**代码解析**：
- 时间复杂度：O(2^n · (n + m))，其中 n ≤ 13，m 为边数
- 空间复杂度：O(n + m)，邻接表 + 递归栈

---

## 总体总结

### 当天重点

- 掌握 **位掩码枚举子集** 的核心技巧，将组合问题转化为位运算问题
- 理解 **异或判断奇偶性** 的数学原理：偶数个 1 的异或结果为 0
- 学会在 **小规模图（n ≤ 13）** 上使用暴力枚举结合连通性验证的解题思路

### 学习收获

- 巩固了位运算在算法设计中的应用（位掩码、异或、位移）
- 掌握了图论中诱导子图（induced subgraph）连通性判断的标准方法
- 理解了复杂度上界分析：2^13 的枚举规模在现代 CPU 上完全可行

### 改进方向

- 可进一步优化：预处理每个子集的连通性，避免重复计算
- 可尝试记忆化搜索（DP + 状态压缩）提升大数据表现

### 明日计划

- 继续每日一题的刷题节奏
- 尝试解决更多 Hard 级别的图论与动态规划综合题

---

*总结日期: 2026-04-27*  
*总通过题目: 持续积累中*  
*主要知识点: 图论、位运算、DFS、子集枚举、连通性判断*