# 练习

## 基础练习

1. 建 `INDEX(city, name)`，跑 `SELECT name FROM user WHERE city = '北京'`——用 EXPLAIN 看 Extra 是否出现 Using index。

2. 同样的索引，跑 `SELECT * FROM user WHERE city = '北京'`——Using index 还在吗？

## 进阶练习

1. `SELECT id FROM user WHERE name = '张三'`——有 `INDEX(name)`，这算覆盖索引吗？

## 答案

1. 有 Using index——name 和 city 都在索引里，不用回表。

2. 不见了——`*` 需要所有列，`INDEX(city, name)` 只有两列。

3. 算。`INDEX(name)` 的叶子节点存 `(name, id)`——id 是主键，天然包含在二级索引里。只查 id 时直接返回，不回表。
