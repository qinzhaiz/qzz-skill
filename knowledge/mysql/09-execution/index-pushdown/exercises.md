# 练习

## 基础练习

1. 建一张有联合索引 `(a, b, c)` 的表，插入数据后分别查询 `WHERE a = 1 AND c = 3`。用 EXPLAIN 观察 Extra 列，确认 ICP 是否生效。

2. 同一张表，查询 `WHERE a = 1 AND d = 4`（d 不在索引中）。ICP 能下推 d 的条件吗？观察 Extra 列。

## 进阶练习

1. 设计一个实验，通过 `EXPLAIN ANALYZE` 测量 ICP 开启和关闭时的查询耗时差异。说明什么情况下差异最明显。

2. 索引下推和覆盖索引是什么关系？能否同时生效？

## 答案

1. 查询 `WHERE a = 1 AND c = 3`，Extra 显示 `Using index condition`——ICP 生效。因为 c 在联合索引中，可以下推到存储引擎判断。

2. d 不在索引中 → ICP 不能下推 d 的条件 → Extra 显示 `Using where`。存储引擎只能按 a=1 过滤，d=4 留给 Server 层。

3. ICP 在回表代价高时最有效——比如 `LIKE 'prefix%'` 的范围扫描，如果 where 条件中索引列能过滤掉大部分数据，ICP 减少的回表次数 → 性能提升明显。

4. 覆盖索引不需要 ICP。ICP 的作用是减少回表次数，覆盖索引直接消除了回表。两者目的相同（减少 IO），手段不同。如果 SELECT 列全在索引中，EXPLAIN 会显示 `Using index`（覆盖索引），ICP 不参与。
