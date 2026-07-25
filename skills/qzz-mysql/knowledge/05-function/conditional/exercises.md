# 练习

## 基础练习

1. 给用户按年龄段分组（<18/18-30/30-50/50+），统计每组多少人。

2. 用 IFNULL 处理 LEFT JOIN 返回的 NULL 值。

3. COALESCE('', '兜底') 和 IFNULL('', '兜底') 的区别？试试看。

## 进阶练习

1. 写一个行转列查询：按月统计各状态（'pending','done','cancelled'）的订单数。

## 答案

1. `SELECT CASE WHEN age<18 THEN '少年' ... END AS grp, COUNT(*) FROM user GROUP BY grp;`

2. `SELECT u.name, IFNULL(o.amount, 0) FROM user u LEFT JOIN orders o ON ...`

3. COALESCE 可以传多个参数，IFNULL 只能两个。但两者的关键区别：空串 `''` 不是 NULL，两者都不会替换空串。
