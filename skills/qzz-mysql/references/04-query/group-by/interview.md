# 面试题

## Q1：WHERE 和 HAVING 的区别？

**考点**：几乎必问。

**回答**：WHERE 过滤行——在分组前执行，能用索引。HAVING 过滤组——在分组后执行，不能用索引。WHERE 不能接聚合函数（COUNT、SUM 等），HAVING 才能。

**加分**：说出执行顺序——`FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`。

## Q2：GROUP BY 为什么要遵守 ONLY_FULL_GROUP_BY？

**考点**：理解 SQL 标准，不是只会写。

**回答**：如果 SELECT 里有一个不在 GROUP BY 中的非聚合列，MySQL 不知道该返回哪一行的值——同一组内有多行。关掉这个限制会导致 MySQL 随机挑一个值，结果不可预测。所以 8.0 默认开启。
