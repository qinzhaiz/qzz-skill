# 代码示例

## 示例 1：配置慢查询日志

```sql
-- 开发环境：阈值 0.1 秒，记录所有可能优化的查询
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 0.1;
SET GLOBAL log_queries_not_using_indexes = ON;
SET GLOBAL min_examined_row_limit = 0;  -- 开发环境全记录

-- 生产环境：阈值 1 秒，只记录真正慢的
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 1;
SET GLOBAL log_queries_not_using_indexes = ON;
SET GLOBAL min_examined_row_limit = 1000;
```

## 示例 2：慢查询日志格式

**场景**：真实慢查询日志的一行记录。

```text
# Time: 2024-07-25T10:30:00.123456Z
# User@Host: root[root] @ localhost []
# Query_time: 2.503452  Lock_time: 0.000123  Rows_sent: 100  Rows_examined: 100000
SET timestamp=1721902200;
SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at LIMIT 100;
```

**解读**：
- `Query_time: 2.5s` — 这条查询执行了 2.5 秒
- `Lock_time: 0.0001s` — 几乎没花时间等锁（锁不是问题）
- `Rows_sent: 100` / `Rows_examined: 100000` — 扫描了 10 万行只返回 100 行（**典型的索引问题**）
- 优化方向：给 `(status, created_at)` 建联合索引

## 示例 3：用 mysqldumpslow 分析

```bash
# 按查询时间排序，看最慢的 10 条
$ mysqldumpslow -s t -t 10 /var/log/mysql/slow.log

Reading mysql slow query log from /var/log/mysql/slow.log

Count: 152  Time=3.52s (535s)  Lock=0.00s (0s)  Rows=100.0 (15200)
  SELECT * FROM orders WHERE status = 'S' ORDER BY created_at LIMIT N

Count: 89  Time=2.15s (191s)  Lock=0.01s (1s)  Rows=0.0 (0)
  UPDATE inventory SET quantity = quantity - N WHERE product_id = N
```

**解读**：
- 第一条：执行了 152 次，平均每次 3.52 秒，累计浪费 535 秒。优先解决。
- 第二条：执行了 89 次，平均 2.15 秒。次优先级。

## 示例 4：监控慢查询数量

```sql
-- 当前总慢查询数
SHOW GLOBAL STATUS LIKE 'Slow_queries';

-- 看过去一分钟新增了多少（需结合计时）
-- 或设置定时任务每分钟查询一次变化量
```

```bash
# 用 cron 监控：每分钟检查是否有大量慢查询
*/1 * * * * mysql -e "SHOW GLOBAL STATUS LIKE 'Slow_queries';" | tail -1
```
