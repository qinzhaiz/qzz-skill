# 练习

## 基础练习

1. 统计 user 表的总行数、平均年龄、最大最小年龄。

2. 按城市分组统计用户数和平均年龄。

## 进阶练习

1. `COUNT(*)` 和 `COUNT(1)` 哪个快？用 EXPLAIN 试试。

2. 为什么 `SELECT city, COUNT(*) FROM user` 不加 GROUP BY 在 8.0 报错？

## 答案

1. `SELECT COUNT(*), AVG(age), MAX(age), MIN(age) FROM user;`

2. `SELECT city, COUNT(*), AVG(age) FROM user GROUP BY city;`

3. 一样快——MySQL 优化器会把 `COUNT(1)` 转成和 `COUNT(*)` 一样的执行计划。

4. 8.0 默认 ONLY_FULL_GROUP_BY——有聚合列时非聚合列必须出现在 GROUP BY 中。
