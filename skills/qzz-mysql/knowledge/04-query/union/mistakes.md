# 常见错误

## 错误 1：UNION 两边列数不同

**症状**：`ERROR 1222: The used SELECT statements have a different number of columns`

**原因**：UNION 要求两边 SELECT 的列数一致。

**怎么修**：缺的列用 NULL 或常量占位。

## 错误 2：习惯性用 UNION 而不是 UNION ALL

**症状**：查询不需要去重但用了 UNION。

**原因**：不知道 UNION 会去重（排序 + 比较），也不知道 UNION ALL 更快。

**怎么修**：确定两边不会重复时用 UNION ALL——跳过排序去重，速度快很多。

## 错误 3：用 UNION 代替 JOIN

**症状**：写了一个很长的 UNION 来拼接不同表的列。

**原因**：没搞清楚 JOIN 是横着拼（加列），UNION 是竖着拼（加行）。

**怎么修**：需要横着拼列 → JOIN。需要竖着拼行 → UNION。
