# 练习

## 基础练习

1. 用 `EXPLAIN` 查看 `SELECT * FROM user WHERE name = 'test'` 的执行计划。观察 `type` 和 `key` 字段的值。如果 name 列没有索引，type 会是什么？

2. 解释 `EXPLAIN` 输出中 `type` 的各种取值的含义：`const`、`ref`、`range`、`ALL`。从快到慢排序。

## 进阶练习

1. 建一张有多个索引的表，写一条能用多个索引的查询。分别用 `EXPLAIN` 和 `optimizer_trace` 看优化器选了哪个，并读懂 `considered_execution_plans`。

2. 为什么 MySQL 8.0 删除了查询缓存？设计一个场景说明查询缓存在实际生产中几乎没用。

## 答案

1. 如果 name 没有索引，`type=ALL`（全表扫描），`key=NULL`。这说明优化器无法用任何索引加速查询。

2. 从快到慢：`const`（主键等值，1 行）> `ref`（索引等值，少量行）> `range`（索引范围）> `ALL`（全表）。还有 `eq_ref`（JOIN 时被驱动表用主键）和 `index`（扫描整个索引但不回表）等。

3. 查询缓存的问题：缓存的键是 SQL 字符串，字符串完全相同才能命中。而且表上任何一次 UPDATE/INSERT/DELETE 都会把这张表的所有缓存全部清空。生产环境中表更新频繁，缓存的命中率极低，维护开销反而拖累性能。

4. optimizer_trace 中 `"considered_execution_plans"` 会列出每个可能的执行计划。每个计划有 `"cost"` 字段表示估算代价。优化器选代价最小的。
