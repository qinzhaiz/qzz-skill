# 练习

## 基础练习

1. 建一张测试表（插入 10 万行），分别执行 `SELECT * FROM t ORDER BY id LIMIT 90000, 10` 和 `SELECT * FROM t WHERE id > 90000 ORDER BY id LIMIT 10`，对比执行时间。

2. 写出 3 种会导致索引失效的 SQL 写法，并给出修正方案。

## 进阶练习

1. 写一个存储过程，实现安全的批量删除（每次 1000 行，间隔 0.5 秒）。在测试表上验证效果。

2. 设计一个场景：一个 JOIN 查询很慢（被驱动表没有索引），用 EXPLAIN 诊断，加索引后对比执行时间。

## 答案

1. 大偏移量方案明显更慢——`LIMIT 90000, 10` 需要扫描前 90010 行再丢弃。基于主键的 `WHERE id > 90000` 直接从索引定位到起点。

2. 三种写法：(a) 索引列用函数 `WHERE YEAR(col) = 2024` → 改为范围查询，(b) 隐式类型转换 `WHERE varchar_col = 数字` → 加引号，(c) 前导模糊 `LIKE '%abc'` → 改为全文搜索或 ES。

3. 使用 `LOOP` 或 `WHILE` + `ROW_COUNT()` + `SLEEP()` 实现分批循环。关键在于每批之间有间隔，防止长时间持锁。

4. 被驱动表无索引 → JOIN 使用 BNL 算法（Type: ALL, Extra: Using join buffer），非常慢。给被驱动表的关联字段加索引后 → NLJ 算法（Type: ref），快几十倍。
