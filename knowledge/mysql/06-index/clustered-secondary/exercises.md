# 练习

## 基础练习

1. 用 `SHOW INDEX FROM user` 看的输出，PRIMARY 和普通索引在 Cardinality 列上有什么区别？

2. 建一张表不设 PRIMARY KEY，用 `SHOW CREATE TABLE` 看 MySQL 有没有自动生成什么。

## 进阶练习

1. `SELECT id FROM user WHERE name = '张三'` ——这条查询需要回表吗？为什么？

## 答案

1. PRIMARY 的基础区分度通常等于行数（每一行一个唯一值），但 InnoDB 的基数统计是抽样估算的，不一定精确。

2. 会生成一个隐式的 `GEN_CLUST_INDEX`（6 字节的 ROW_ID）。每张 InnoDB 表必须有聚簇索引。

3. 不需要。`id` 就是主键——二级索引 name 的叶子节点存的正是 (name, id)。只查 id 时直接从二级索引返回，不用回表。这就是一种覆盖索引。
