# 练习

## 基础练习

1. 查出年龄最小的 3 个用户。

2. 查出用户列表，按城市升序、同城按创建时间降序排列。

3. 实现分页：每页 3 条，查出第 2 页数据。

## 进阶练习

1. 用 `EXPLAIN` 比较 `LIMIT 10 OFFSET 100000` 和 `WHERE id > 100000 LIMIT 10` 的 rows 差异。

2. 如果主键不是自增 INT 而是 UUID，游标分页还能用吗？为什么？

## 答案

1. `SELECT * FROM user ORDER BY age LIMIT 3;`

2. `SELECT * FROM user ORDER BY city, created_at DESC;`

3. `SELECT * FROM user ORDER BY id LIMIT 3 OFFSET 3;`

4. 游标分页在 UUID 主键下不可靠——UUID 无序，无法保证"大于上一页最后一条"就能覆盖所有后续数据。
