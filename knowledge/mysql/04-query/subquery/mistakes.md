# 常见错误

## 错误 1：NOT IN + NULL

**症状**：`WHERE id NOT IN (SELECT user_id FROM orders)` 从不返回结果。

**原因**：子查询结果里有 NULL——`id != NULL` 结果是 UNKNOWN。WHERE 只要不是 TRUE 就过滤掉。

**怎么修**：子查询里加 `WHERE col IS NOT NULL`，或用 NOT EXISTS。

## 错误 2：标量子查询返回了多行

**症状**：`ERROR 1242 (21000): Subquery returns more than 1 row`

**原因**：标量子查询（用在 =、>、< 后面的子查询）必须返回恰好一行一列。多行了 MySQL 不知道该选哪个。

**怎么修**：改成 IN 或 EXISTS，或者加 LIMIT 1 限制行数。

## 错误 3：子查询性能不如 JOIN

**症状**：复杂的嵌套子查询在数据量大了之后变慢。

**原因**：MySQL 5.7 以前子查询优化不好，经常导致全表扫描。8.0 改善了很多，但复杂子查询仍可能不如 JOIN。

**怎么修**：写完之后看 EXPLAIN。如果子查询被优化成了"物化扫描"，考虑改成 JOIN。
