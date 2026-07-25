# SQL 优化

> 写出正确的 SQL 不难，写出快的 SQL 才是本事——几个常见场景的优化技巧。

## 为什么需要它

EXPLAIN 告诉你了"这里有问题"，慢查询日志告诉你了"这条 SQL 很慢"，然后呢？SQL 优化就是"然后"——针对常见性能问题，有成熟的解决方案。

## 它是什么

SQL 优化是集合了多种技巧的工具箱——覆盖排序、分页、JOIN、COUNT、删除等常见"慢"场景。每个场景都有套路。

## 六大优化场景

### 1. ORDER BY 优化——让排序走索引

索引天然有序。如果 ORDER BY 的字段在索引中，且顺序一致，MySQL 不需要额外排序。

```sql
-- 联合索引 (a, b)
SELECT * FROM t ORDER BY a;           -- ✅ 利用索引
SELECT * FROM t ORDER BY a, b;         -- ✅ 利用索引
SELECT * FROM t ORDER BY a DESC, b DESC; -- ✅
SELECT * FROM t ORDER BY a ASC, b DESC;  -- ❌ 方向不一致，filesort
SELECT * FROM t WHERE a = 1 ORDER BY b;  -- ✅ a 等值后 b 天然有序
```

**关键**：`WHERE` 条件是等值（=，IN），然后 `ORDER BY` 是下一个索引列——这种情况索引排序最有效。

### 2. LIMIT 大偏移量优化——先定位再取数

```sql
-- 慢：翻到第 100 万页
SELECT * FROM t ORDER BY id LIMIT 1000000, 20;
-- 数据库要扫描 1000020 行，然后扔掉前 1000000 行

-- 快：用主键定位起点
SELECT * FROM t WHERE id > 1000000 ORDER BY id LIMIT 20;

-- 或：先取 ID（覆盖索引），再 JOIN 回表
SELECT t1.* FROM t t1
JOIN (SELECT id FROM t ORDER BY id LIMIT 1000000, 20) t2
ON t1.id = t2.id;
```

### 3. JOIN 优化——小表驱动大表

- **被驱动表的关联字段必须有索引**（最重要的 JOIN 优化规则）
- 小表做驱动表（`LEFT JOIN` 左边是驱动表，`INNER JOIN` 由优化器决定）
- 只 SELECT 需要的列，不用 `SELECT *`（减少 join buffer 占用）
- 如果优化器选错了驱动表，用 `STRAIGHT_JOIN` 强制指定

### 4. COUNT 优化——别纠结写法

```sql
COUNT(*) = COUNT(1) > COUNT(col)   -- col 不统计 NULL
```
- InnoDB 没有维护精确的总行数（MVCC 导致）。每次 COUNT 都要扫描。
- 如果不需要精确值，用 `SHOW TABLE STATUS` 看估算值
- 如果需要精确高频计数，用 Redis 计数器或单独维护计数表

### 5. 分批删除——避免长时间锁表

```sql
-- 不要一次删除 100 万行（长事务 + 锁太多行）
DELETE FROM logs WHERE created_at < '2024-01-01';

-- 分批删，每次 1000 行
DELETE FROM logs WHERE created_at < '2024-01-01' LIMIT 1000;
-- 循环执行直到 affected_rows = 0
-- 每次之间有间隔，让其他事务有机会执行
```

### 6. 避免索引失效

```sql
-- ❌ 索引列用函数
WHERE YEAR(created_at) = 2024        -- 改为：WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'

-- ❌ 隐式类型转换
WHERE phone = 13800000000            -- phone 是 VARCHAR → 改为：WHERE phone = '13800000000'

-- ❌ 前导模糊
WHERE name LIKE '%张三'              -- 无法用索引。改为全文搜索或 ES

-- ❌ OR 连接非索引列
WHERE a = 1 OR b = 2                 -- 如果 b 没索引，不会走 a 的索引。改为 UNION
```

## 怎么用

优化没有银弹——每次优化都要走这个流程：

1. 定位慢 SQL（慢查询日志）
2. 用 EXPLAIN 分析为什么慢（没走索引？扫太多行？用了临时表？）
3. 针对问题选优化方案（上面六大场景之一）
4. 用 EXPLAIN 验证优化效果
5. 上生产后继续监控

## 注意事项

1. **优化前先确认数据量和业务场景**——开发环境 100 行全表扫很快，生产环境 100 万行就不一样了。
2. **优化后要测试**——一个索引可能加速查询但拖慢写入（索引维护有代价）。
3. **有些"慢"是正常的**——报表统计需要扫全表做聚合，这是业务需求而不是性能问题。

## 和什么有关

- [EXPLAIN 执行计划](../explain/) —— 优化前必须看的诊断工具
- [慢查询日志](../slow-query/) —— 发现需要优化的 SQL
- [索引优化](../../06-index/optimization/) —— 大部分 SQL 优化最终是加索引
- [JOIN 查询](../../04-query/join/) —— JOIN 优化详解
