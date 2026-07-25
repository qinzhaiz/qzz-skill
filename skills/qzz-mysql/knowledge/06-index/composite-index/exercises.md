# 练习

## 基础练习

1. 建 `idx_city_age`，测试 `WHERE city = '北京' AND age > 20` 和 `WHERE age > 20 AND city = '北京'` 是否都走索引。

2. 建 `idx_a_b_c`，测试 `WHERE b = 2` 是否走索引。

## 进阶练习

1. 设计一个查询 `WHERE city = '北京' ORDER BY age LIMIT 10`——最合适的索引是什么？建了之后用 EXPLAIN 验证是否出现 filesort。

## 答案

1. 两个都走索引——MySQL 优化器自动调整条件顺序以匹配索引，跟书写顺序无关。

2. 不走——跳过 a，索引失效。

3. `INDEX(city, age)`——city 过滤，age 直接排序，无 filesort。
