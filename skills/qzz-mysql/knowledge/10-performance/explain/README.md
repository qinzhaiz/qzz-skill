# EXPLAIN 执行计划

> 写出 SQL 只是第一步，会用 EXPLAIN 看它怎么跑才是真正学会了 SQL。

## 为什么需要它

同样的功能，不同写法性能可能差几百倍。你看不出差别——数据库看起来都正常返回了结果。EXPLAIN 就是让你看到"数据库后台是怎么执行你的 SQL 的"：用了哪个索引、扫了多少行、是不是用了临时表。

## 它是什么

EXPLAIN 是 MySQL 的查询分析工具——在 SQL 前面加 `EXPLAIN`，MySQL 会告诉你**优化器决定怎么执行这条 SQL**，而不是实际去执行它。

## 怎么工作

```sql
EXPLAIN SELECT * FROM user WHERE id = 1;
```sql

输出一张表，每行代表一个执行步骤。最关键的 4 列：

| 列 | 含义 | 怎么看 |
|----|------|--------|
| **type** | 访问方式 | ALL 最差 → index → range → ref → eq_ref → const 最好 |
| **key** | 实际使用的索引 | 看看是不是你建的那个？NULL 表示没用索引 |
| **rows** | 预估扫描行数 | 越小越好（但只是估算，不精确） |
| **Extra** | 额外信息 | `Using index` 好，`Using filesort` / `Using temporary` 需要关注 |

### type 从好到差

```sql
system → const → eq_ref → ref → range → index → ALL
  1行   主键=1行 JOIN主键  普通索引  索引范围  全索引扫  全表扫
```sql

日常开发：
- `const` 或 `eq_ref`：非常好，不需要优化
- `ref` 或 `range`：正常，大部分查询就这个水平
- `index`：虽然用了索引但扫了全索引——注意一下
- `ALL`：全表扫描——**必须优化**（加索引或改 SQL）

### Extra 关键标记

| Extra | 含义 | 建议 |
|-------|------|------|
| `Using index` | 覆盖索引——不用回表 | ✅ 理想 |
| `Using index condition` | 索引下推 | ✅ 不错 |
| `Using where` | Server 层做了过滤 | 中性，看 rows 判断 |
| `Using filesort` | 需要额外排序 | ⚠️ 加索引优化 ORDER BY |
| `Using temporary` | 用了临时表 | ⚠️ GROUP BY/DISTINCT/UNION 可能慢 |
| `Using join buffer` | JOIN 时被驱动表没索引 | ⚠️ 给被驱动表加索引 |

## 怎么用

```sql
-- 基础用法
EXPLAIN SELECT * FROM user WHERE email = 'test@example.com';

-- MySQL 8.0.18+：看实际执行情况（会真的执行 SQL）
EXPLAIN ANALYZE SELECT * FROM user WHERE email = 'test@example.com';
-- 输出：实际耗时、实际扫描行数、是否用了循环嵌套

-- 看更详细的代价评估
EXPLAIN FORMAT=JSON SELECT * FROM user WHERE email = 'test@example.com';

-- 看 UPDATE/DELETE/INSERT 的执行计划
EXPLAIN DELETE FROM user WHERE created_at < '2024-01-01';

-- 结合 SHOW WARNINGS 看优化器重写后的 SQL
EXPLAIN SELECT * FROM user WHERE name = 'test';
SHOW WARNINGS;  -- 看看优化器把 SQL 改成了什么样
```sql

## 注意事项

1. **EXPLAIN 只是预估，不是实际执行**——`rows` 可能不准（统计信息过时）。用 `EXPLAIN ANALYZE` 看实际结果。
2. **EXPLAIN 不会执行你的 SQL**（除了 EXPLAIN ANALYZE）——所以 `EXPLAIN DELETE` 不会真的删数据。
3. **Extra 列有多个值时一起看**——比如 `Using index; Using where` 表示覆盖索引 + Server 层过滤，虽然不用回表但有些行被过滤了。

## 和什么有关

- [索引基础](../../06-index/what-is-index/) —— 看懂 type 和 key 的前提
- [覆盖索引](../../06-index/covering-index/) —— `Using index` 的含义
- [索引下推](../../09-execution/index-pushdown/) —— `Using index condition` 的含义
- [SQL 优化](../sql-optimization/) —— EXPLAIN 发现问题后怎么改
