# 练习

## 基础练习

1. 在 user 表的 city 列上建索引，用 EXPLAIN 验证查询 `WHERE city = '北京'` 是否用上。

2. 删除刚建的索引，再用 EXPLAIN 对比前后差异。

3. 用 `SHOW INDEX FROM user` 看表上有哪些索引。

## 进阶练习

1. 往 user 表插入 10 万行测试数据，对比建索引前后 `SELECT * FROM user WHERE name = 'xxx'` 的执行时间。

## 答案

1-3 无标准答案。

4. 建索引后通常快 100-1000 倍——全表扫 vs 几次 IO 的差距。
