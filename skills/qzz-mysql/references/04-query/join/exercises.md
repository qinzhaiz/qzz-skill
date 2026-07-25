# 练习

## 基础练习

1. 查出所有订单，同时显示下单用户的姓名。

2. 查出所有用户和他们的订单数（含没有订单的用户，显示 0）。

3. INNER JOIN 和 LEFT JOIN 的区别是什么？写两个查询验证。

## 进阶练习

1. 三张表 JOIN：用户 → 订单 → 商品，查出每个订单对应的商品名。

2. 用 EXPLAIN 比较被驱动表有索引和没索引的 JOIN 性能差异。

## 答案

1. `SELECT u.name, o.* FROM user u JOIN orders o ON u.id = o.user_id;`

2. `SELECT u.name, COUNT(o.id) FROM user u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id;`

3. INNER JOIN 只返回两表都匹配的行。LEFT JOIN 左表全保留，右表没匹配的填 NULL。
