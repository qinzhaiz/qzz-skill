# 练习

## 基础练习

1. 对 `SELECT * FROM user WHERE age > 20 ORDER BY created_at LIMIT 10` 执行 EXPLAIN。如果 type=ALL、Extra=Using filesort，该怎么优化？

2. 建一张表，分别执行有索引和无索引的 GROUP BY 查询，对比 EXPLAIN 的 `Extra` 列输出。

## 进阶练习

1. 用 EXPLAIN FORMAT=JSON 分析一条 JOIN 查询，找出 "cost_info" 部分，解读每个步骤的预估代价。

2. 用 EXPLAIN ANALYZE 比较同一查询在不同索引策略下的实际执行时间。

## 答案

1. 需要加复合索引 `(age, created_at)`——age 用于 WHERE 过滤（range 扫描），created_at 用于排序（索引有序，避免 filesort）。加索引后 EXPLAIN 的 type 应该变成 range，Extra 不再有 Using filesort。

2. 无索引时 GROUP BY 用临时表：`Extra: Using temporary; Using filesort`。有索引时利用索引有序性直接分组：`Extra: Using index`。

3. cost_info 中的 `"query_cost"` 是总代价，`"read_cost"` 是 IO 代价，`"eval_cost"` 是计算代价。优化器选 query_cost 最小的方案。

4. EXPLAIN ANALYZE 会显示每步的 `actual time` 和 `actual rows`，可以和 EXPLAIN 的 `rows`（预估）对比，判断统计信息是否准确。
