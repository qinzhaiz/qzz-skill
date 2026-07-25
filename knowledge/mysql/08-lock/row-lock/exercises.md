# 练习

## 基础练习

1. 终端 A 执行 `SELECT * FROM user WHERE id = 1 FOR UPDATE`（事务中，不提交），终端 B 执行 `SELECT * FROM user WHERE id = 1 FOR UPDATE`。B 会阻塞吗？换成 `FOR SHARE` 呢？

2. 终端 A `SELECT * FROM user WHERE id BETWEEN 5 AND 10 FOR UPDATE`（RR 级别），终端 B 插入 `id=7` 会阻塞吗？插入 `id=11` 呢？

## 进阶练习

1. 建一张有索引和没索引的表。分别测试：WHERE 条件命中索引 vs 全表扫描，观察锁的范围差异。

2. 查 `performance_schema.data_locks` 表，看看 Next-Key Lock 实际加了哪些锁。

## 答案

1. 会阻塞——FOR UPDATE 是排他锁（X），两个 X 锁互斥。FOR SHARE 不阻塞——共享锁（S）之间不互斥。

2. id=7 在范围 `(5, 10]` 内 → 阻塞。id=11 不在范围内 → 不阻塞（具体取决于查询锁定的 Next-Key 区间）。

3. 命中索引 → 只锁符合条件的行。全表扫描 → `performance_schema.data_locks` 显示所有行都被锁。

4. `SELECT * FROM performance_schema.data_locks` 可以看到 LOCK_TYPE（RECORD）、LOCK_MODE（X）、LOCK_DATA（被锁的索引值）。
