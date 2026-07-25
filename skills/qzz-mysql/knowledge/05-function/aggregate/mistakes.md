# 常见错误

## 错误 1：在 WHERE 里用聚合函数

**症状**：`WHERE COUNT(*) > 5` 报错。

**原因**：聚合函数在分组之后才计算——WHERE 在分组之前执行。

**怎么修**：用 HAVING。

## 错误 2：COUNT(col) 忽略了 NULL

**症状**：`SELECT COUNT(phone) FROM user` 返回 95，以为是 100。

**原因**：phone 列有 5 个 NULL——COUNT(col) 不计 NULL 值。

**怎么修**：统计行数用 COUNT(*)，统计某列非空值数才用 COUNT(col)。

## 错误 3：SUM/AVG 在空结果上返回 NULL

**症状**：`SELECT SUM(amount) FROM orders WHERE user_id = 999` 返回 NULL（不存在这个用户）。

**原因**：没有符合条件的行时，聚合函数除 COUNT 外返回 NULL。

**怎么修**：应用层判空，或用 `IFNULL(SUM(amount), 0)`。
