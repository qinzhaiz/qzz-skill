# 练习

## 基础练习

1. 用 CTE 查出北京用户中年龄大于 20 的人。

2. 用多个 CTE 串联：先筛大额订单，再按用户汇总，最后 JOIN 用户名。

## 进阶练习

1. 用递归 CTE 展开一个多层分类表（category 表：id、name、parent_id）。

## 答案

1. `WITH bu AS (SELECT * FROM user WHERE city='北京') SELECT * FROM bu WHERE age>20;`

2. 见 examples 示例 2。

3. 见 examples 示例 3——把 employee 换成 category、manager_id 换成 parent_id 即可。
