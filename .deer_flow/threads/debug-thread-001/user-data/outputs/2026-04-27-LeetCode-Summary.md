# 2026-04-27 LeetCode 刷题总结

## 概述

今日完成 **每日一题**，成功通过第 **1391** 题《检查网格中是否存在有效路径》。

---

## 当天统计

| 难度等级 | 数量 | 占比 |
|---------|------|------|
| Medium | 1 | 100% |

**主要知识点分布**：深度优先搜索 (DFS)、广度优先搜索 (BFS)、并查集 (Union Find)、数组、矩阵

---

## 题目总结

### 1. 检查网格中是否存在有效路径

**题目ID**: 1391  
**题目链接**: https://leetcode.cn/problems/check-if-there-is-a-valid-path-in-a-grid/

**难度**: Medium | **知识点**: DFS/BFS, Union Find, Array, Matrix

**关联公司**: Samsung, Robinhood, Amazon

**状态**: ✅ 已通过 (AC)

**提交信息**:
- 提交ID: 721408243
- 语言: Python3
- 耗时: 167 ms
- 内存: 54.9 MB

**题目描述**:
给你一个 `m x n` 的网格 `grid`。网格里的每个单元都代表一条街道。`grid[i][j]` 的街道可以是：

- `1` 表示连接左单元格和右单元格的街道
- `2` 表示连接上单元格和下单元格的街道
- `3` 表示连接左单元格和下单元格的街道
- `4` 表示连接右单元格和下单元格的街道
- `5` 表示连接左单元格和上单元格的街道
- `6` 表示连接右单元格和上单元格的街道

如果可以从左上角 `(0, 0)` 通过街道到达右下角 `(m - 1, n - 1)`，返回 `true`，否则返回 `false`。

**难点分析**:
- 需要理解每种街道类型对应的连接方向
- 判断相邻单元格之间是否能够互相连通
- 图的遍历问题，需要选择合适的搜索策略

**解题思路**:
1. **并查集方法**: 将相邻可连通的单元格合并，最后判断起点和终点是否在同一集合
2. **DFS/BFS方法**: 从起点开始，按照街道规则进行搜索，判断是否能到达终点

**解题代码**:

```python
class Solution:
    def hasValidPath(self, grid: List[List[int]]) -> bool:
        # 方法1: 并查集
        m, n = len(grid), len(grid[0])
        parent = list(range(m * n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # 根据街道类型确定连接方向
        dirs = {
            1: [(0, -1), (0, 1)],   # 左、右
            2: [(-1, 0), (1, 0)],   # 上、下
            3: [(0, -1), (1, 0)],   # 左、下
            4: [(0, 1), (1, 0)],    # 右、下
            5: [(0, -1), (-1, 0)], # 左、上
            6: [(0, 1), (-1, 0)],  # 右、上
        }
        
        for i in range(m):
            for j in range(n):
                idx = i * n + j
                for di, dj in dirs[grid[i][j]]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n:
                        # 检查对面单元格是否连接到当前单元格
                        if self.can_connect(grid[i][j], grid[ni][nj], di, dj):
                            union(idx, ni * n + nj)
        
        return find(0) == find(m * n - 1)
    
    def can_connect(self, cur, next_val, di, dj):
        # 判断两个单元格是否能够连通
        # cur 单元格通过 (di, dj) 方向连接到 next 单元格
        # next 单元格需要通过相反方向连接到 cur
        opposite = (-di, -dj)
        rev_dirs = {
            1: [(0, -1), (0, 1)],
            2: [(-1, 0), (1, 0)],
            3: [(0, -1), (1, 0)],
            4: [(0, 1), (1, 0)],
            5: [(0, -1), (-1, 0)],
            6: [(0, 1), (-1, 0)],
        }
        return opposite in rev_dirs.get(next_val, [])
```

---

## 总体总结

### 当天重点
- 今日完成网格路径连通性判断问题
- 重点掌握并查集或搜索算法在网格问题中的应用

### 学习收获
- 理解了街道类型的方向表示方式
- 掌握了并查集在连通性判断问题中的应用
- 复习了图搜索的基本方法

### 改进方向
- 尝试多种解法，比较时间空间复杂度
- 巩固并查集的路径压缩和按秩合并优化

### 明日计划
- 继续保持每日一题的节奏
- 尝试更多中等难度的搜索类题目

---

*总结日期: 2026-04-27*  
*总通过题目: 1391*  
*主要知识点: DFS, BFS, Union Find, Array, Matrix*