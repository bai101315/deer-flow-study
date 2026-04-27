---
name: get-leetcode-timestamp
description: 自动获取当前时间、1天前、7天前的标准时间戳。适配 LeetCode：UTC 秒级时间戳 + 东八区时区修正
trigger:
  - 获取时间戳
  - get timestamp
  - LeetCode 时间
  - 时间范围
  - timestamp
---

# Get LeetCode Timestamp Skill

自动获取当前时间、1 天前、7 天前的标准时间戳。适配 LeetCode：UTC 秒级时间戳 + 东八区时区修正。

## 实现代码

```javascript
// 适配 LeetCode：UTC 秒级时间戳 + 东八区时区修正
function getLeetCodeTimeRange() {
  // 时区：中国东八区（UTC+8），LeetCode 使用 UTC 时间
  const TIME_ZONE_OFFSET = 8 * 60 * 60; 
  // 当前秒级时间戳（UTC）
  const now = Math.floor(Date.now() / 1000) - TIME_ZONE_OFFSET;
  
  return {
    // 当前时间
    currentTime: now,
    // 1天前（24小时）
    oneDayAgo: now - 24 * 60 * 60,
    // 7天前（1周）
    sevenDaysAgo: now - 7 * 24 * 60 * 60
  };
}
```

## 使用示例

可直接用于 LeetCode API 调用：
- `leetcode_get_all_submissions` 的 `startTime` 参数
- 查询今天/昨天/近7天解决的题目数量

## 返回值说明

| 字段 | 说明 |
|------|------|
| currentTime | 当前时间（秒级时间戳，东八区修正） |
| oneDayAgo | 1天前的时间戳 |
| sevenDaysAgo | 7天前的时间戳 |