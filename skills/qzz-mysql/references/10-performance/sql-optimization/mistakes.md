# 常见错误

## 错误 1：只要慢就加索引

**症状**：表上建了十几个索引，查询还是慢，写入反而更慢了。

**原因**：索引不是免费的——每次 INSERT/UPDATE/DELETE 都要维护所有索引。索引过多 → 写入变慢，而且优化器可能选错索引。不是所有慢查询都需要新索引。

**怎么修**：先看 EXPLAIN，确认现有索引为什么没被用上。可能是 SQL 写法导致索引失效（函数、类型转换），而不是缺索引。优化 SQL 写法 > 加新索引。

## 错误 2：任何时候都用 `SELECT *`

**症状**：查询慢，JOIN 特别慢。

**原因**：`SELECT *` 返回所有列 → (1) 覆盖索引不可能生效（必须回表），(2) JOIN 时大量无用数据通过 join buffer，(3) 网络传输更多数据。

**怎么修**：只 SELECT 需要的列。如果业务确实需要大部分列，至少在大表 JOIN 时用子查询先筛选 ID，再 JOIN 取完整行。

## 错误 3：ORDER BY RAND() 随机取数据

**症状**：`SELECT * FROM t ORDER BY RAND() LIMIT 10` 在大表上极慢。

**原因**：`ORDER BY RAND()` 给每一行生成一个随机数，然后排序——全表扫描 + 排序。100 万行就是给 100 万行分配随机数再排序。

**怎么修**：
- 如果主键连续：`SELECT * FROM t WHERE id >= FLOOR(RAND() * (SELECT MAX(id) FROM t)) LIMIT 10`
- 如果数据量大且不连续：`SELECT * FROM t WHERE id IN (SELECT id FROM t ORDER BY RAND() LIMIT 10)` —— 子查询先随机取 ID（覆盖索引），再回表
- 更简单的方案：应用层生成随机 ID，再查询
