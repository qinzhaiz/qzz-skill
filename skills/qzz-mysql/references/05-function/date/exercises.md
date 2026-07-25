# 练习

## 基础练习

1. 查出今天创建的订单。

2. 按月统计用户注册数（用 DATE_FORMAT）。

3. 查最近 7 天内创建的订单。

## 进阶练习

1. 为什么 `WHERE DATE(created_at) = '2025-07-25'` 很慢？怎么改？

## 答案

1. `SELECT * FROM orders WHERE created_at >= CURDATE() AND created_at < DATE_ADD(CURDATE(), INTERVAL 1 DAY);`

2. `SELECT DATE_FORMAT(created_at, '%Y-%m'), COUNT(*) FROM orders GROUP BY 1;`

3. `SELECT * FROM orders WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY);`

4. 因为对列用函数 → 索引失效。改成范围查询 `WHERE created_at >= ... AND created_at < ...`。
