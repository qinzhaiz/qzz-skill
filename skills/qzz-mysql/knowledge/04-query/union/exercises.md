# 练习

## 基础练习

1. 查出城市是北京或上海的用户，用 UNION 实现。

2. 对比 UNION 和 UNION ALL 返回的行数——有没有差异？

## 进阶练习

1. UNION 和 JOIN 分别适合什么场景？想一个 UNION 不适用的场景。

## 答案

1. `SELECT * FROM user WHERE city='北京' UNION SELECT * FROM user WHERE city='上海';`

2. 如果先两个查询有重复行——UNION 行数 < UNION ALL 行数。如果完全无重复——数量相同但 UNION 更慢。

3. JOIN 是左右拼接（关联），UNION 是上下堆叠（合并）。要横着加列用 JOIN，要竖着加行用 UNION。
