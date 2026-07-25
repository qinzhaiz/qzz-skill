# 练习

## 基础练习

1. 查出年龄比所有用户平均年龄小的用户。

2. 查出下过订单的用户姓名（用 IN 子查询）。

3. 查出没有订单的用户（用 NOT EXISTS）。

## 进阶练习

1. 试试 `SELECT * FROM user WHERE id NOT IN (1, 2, NULL)` 返回什么。解释为什么。

2. 把上面那条改成 NOT EXISTS 写法，对比结果。

## 答案

1. `SELECT name FROM user WHERE age < (SELECT AVG(age) FROM user);`

2. `SELECT name FROM user WHERE id IN (SELECT DISTINCT user_id FROM orders);`

3. `SELECT * FROM user WHERE NOT EXISTS (SELECT 1 FROM orders WHERE user_id = user.id);`

4. NOT IN + NULL = 全空。因为 `id != NULL` 结果是 UNKNOWN（不是 TRUE），UNKNOWN 在 WHERE 中等同 FALSE。
