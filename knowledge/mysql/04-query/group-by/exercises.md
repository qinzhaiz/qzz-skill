# 练习

## 基础练习

1. 查出每个城市的用户数和平均年龄。

2. 查出订单最多的 5 个用户（按 user_id 分组，COUNT 排序，LIMIT 5）。

3. WHAT 和 HAVING 有什么区别？写一个查询验证。

## 进阶练习

1. SELECT 里写了一个不在 GROUP BY 中的列，MySQL 8.0 默认报什么错？怎么改 SQL mode 可以让它不报错（但不推荐）？

## 答案

1. `SELECT city, COUNT(*), AVG(age) FROM user GROUP BY city;`

2. `SELECT user_id, COUNT(*) AS cnt FROM orders GROUP BY user_id ORDER BY cnt DESC LIMIT 5;`

3. WHERE 在分组前过滤行，HAVING 在分组后过滤组。WHERE 不能接聚合函数，HAVING 可以。
