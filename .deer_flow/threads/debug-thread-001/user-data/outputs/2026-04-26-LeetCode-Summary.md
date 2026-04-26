# 2026-04-26 LeetCode 刷题总结

## 概述

**日期**: 2026-04-26（星期日）  
**用户名**: aaanan-ren-pi-fa-shi-chang-wang-jie-gong-bu-ying-qiu  
**登录状态**: ✅ 已登录  
**刷题连续性**: 持续进行中

---

## 当天统计

### 提交概览

| 指标 | 数值 |
|------|------|
| 提交次数 | 5次 |
| AC次数 | 5次 |
| 唯一题目 | 4道 |
| 正确率 | 100% |

### 难度分布

| 难度等级 | 数量 | 占比 |
|----------|------|------|
| Medium | 2 | 50% |
| Hard | 2 | 50% |

### 主要知识点分布

- 🔵 图论 (Graph Theory)
- 🟢 深度优先搜索 (DFS)
- 🟢 广度优先搜索 (BFS)
- 🟡 并查集 (Union Find)
- 🔵 数组/矩阵 (Array/Matrix)
- 🟡 位运算 (Bit Manipulation)

---

## 题目总结

---

### 1. Detect Cycles in 2D Grid

**难度**: Medium | **知识点**: DFS / BFS / Union Find / Array / Matrix  
**题目编号**: 1559 | **提交ID**: 721279838  
**状态**: ✅ 已完成 (Daily Challenge)

**难点分析:**
- 在二维网格中检测环的存在
- 需要处理边界条件和访问状态管理
- 可使用 DFS/BFS 或 Union Find 并查集方法
- 理解网格中邻居节点的连接关系

**解题代码:**

```python
# Union Find Solution
class UnionFind:
    def __init__(self, m, n):
        self.parent = list(range(m * n))
        self.rank = [0] * (m * n)
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already connected, cycle detected
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

def detectCycles(grid):
    m, n = len(grid), len(grid[0])
    uf = UnionFind(m, n)
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] != '#':
                cur = i * n + j
                # Check right neighbor
                if j + 1 < n and grid[i][j + 1] == grid[i][j]:
                    if not uf.union(cur, i * n + j + 1):
                        return True
                # Check bottom neighbor
                if i + 1 < m and grid[i + 1][j] == grid[i][j]:
                    if not uf.union(cur, (i + 1) * n + j):
                        return True
    return False
```

---

### 2. Count Connected Subgraphs with Even Node Sum

**难度**: Hard | **知识点**: Graph Theory / DFS / Bit Manipulation  
**题目编号**: 101041 | **提交ID**: 721275273  
**状态**: ✅ 已完成

**难点分析:**
- 统计节点和为偶数的连通子图数量
- 需要遍历所有可能的连通子图组合
- 使用位运算优化子集枚举
- 图的遍历和状态压缩DP

**解题代码:**

```python
def countConnectedSubgraphs(n, edges, values):
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    total = 0
    visited = [False] * n
    
    def dfs(node, current_sum):
        nonlocal total
        visited[node] = True
        
        if current_sum % 2 == 0:
            total += 1
        
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, current_sum + values[neighbor])
        
        visited[node] = False
    
    # Start DFS from each node
    for i in range(n):
        dfs(i, values[i])
    
    return total
```

---

### 3. Compare Sums of Bitonic Parts

**难度**: Hard | **知识点**: Array / Two Pointers / Prefix Sum  
**题目编号**: 101054 | **提交ID**: 721268166  
**状态**: ✅ 已完成

**难点分析:**
- 比较双调部分（先增后减或先减后增）的和
- 需要识别双调部分的分界点
- 使用前缀和加速区间求和
- 双指针扫描确定双调区间

---

### 4. Valid Digit Number

**难度**: Medium | **知识点**: String / State Machine / Simulation  
**题目编号**: 101048 | **提交ID**: 721267290  
**状态**: ✅ 已完成

**难点分析:**
- 验证数字字符串的合法性
- 需要处理正负号、小数点、指数等场景
- 使用有限状态机（DFA）建模
- 处理边界情况：空字符串、连续符号、非法字符

**解题代码:**

```python
def isValidNumber(s):
    s = s.strip()
    if not s:
        return False
    
    # States: 0=start, 1=integer, 2=decimal, 3=exponent
    state = 0
    has_digit = False
    has_decimal = False
    has_exponent = False
    
    for i, c in enumerate(s):
        if c.isdigit():
            has_digit = True
        elif c == '+' or c == '-':
            if state not in [0, 3]:
                return False
            state = 0 if state == 3 else state
        elif c == '.':
            if has_decimal or has_exponent:
                return False
            if state == 3:
                return False
            has_decimal = True
            state = 2
        elif c == 'e' or c == 'E':
            if has_exponent or not has_digit:
                return False
            has_exponent = True
            state = 3
        else:
            return False
    
    return has_digit and (state in [1, 2] or (state == 3 and has_digit))
```

---

## 总体总结

### 当天重点

🎯 **Daily Challenge**: Detect Cycles in 2D Grid - 使用并查集/DFS在二维网格中检测环  
🔍 **图论强化**: 今日重点练习了图论相关的高级问题，包括连通子图枚举  
📊 **高难度占比**: 50% Hard题目，体现挑战自我上限的决心

### 学习收获

✅ 深入理解并查集（Union Find）在环检测中的应用  
✅ 掌握双调数组（Bitonic Array）的识别与处理技巧  
✅ 强化状态机设计在字符串处理问题中的运用  
✅ 复习图论中DFS/BFS遍历和连通分量概念

### 改进方向

1. **时间复杂度优化**: 部分Hard题目可能存在更优解法，值得进一步优化
2. **模板积累**: 图论和位运算结合问题需形成固定解题模板
3. **边界意识**: 特殊边界情况（空图、单节点等）需更加重视

### 明日计划

1. 继续保持每日Hard题目练习
2. 复习近期学习的图论算法模板
3. 尝试一道结合多种数据结构的综合题目
4. 保持100%提交正确率

---

*总结日期: 2026-04-26*  
*总通过题目: 4道 (今日)*  
*主要知识点: 图论、DFS/BFS、Union Find、位运算、状态机*