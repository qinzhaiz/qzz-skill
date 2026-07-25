# 常见错误

## 错误 1：5.7 上用 CTE

**症状**：`ERROR 1064: You have an error in your SQL syntax`

**原因**：CTE（WITH 子句）是 MySQL 8.0 才引入的。5.7 不支持。

**怎么修**：升级到 8.0，或者用子查询/VIEW 替代。

## 错误 2：递归 CTE 忘了写 RECURSIVE

**症状**：CTE 里引用了自己，但没加 RECURSIVE 关键字。

**原因**：WITH 和 WITH RECURSIVE 是不同的语法——MySQL 需要明确知道这是递归 CTE。

**怎么修**：递归 CTE 必须写 `WITH RECURSIVE`。

## 错误 3：CTE 被当作物理表

**症状**：在一个大查询里多次引用同一个 CTE，期待它只算一次。

**原因**：CTE 是内联展开的——每次引用都重新执行里面的查询。不是缓存。

**怎么修**：如果 CTE 结果被多次引用且计算代价高，考虑用临时表或物化视图替代。
