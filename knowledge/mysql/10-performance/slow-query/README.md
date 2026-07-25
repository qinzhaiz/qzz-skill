# 慢查询日志

> MySQL 的"黑匣子"——记录所有执行太慢的 SQL，告诉你哪里出问题了。

## 为什么需要它

用户说"系统很慢"。但慢在哪里？是某个功能慢？某个时间段慢？还是所有操作都慢？慢查询日志回答了这个问题——**把执行时间超过阈值的 SQL 全部记录下来**，让你有据可查，而不是靠猜。

## 它是什么

慢查询日志（Slow Query Log）是 MySQL 内置的诊断工具。当一条 SQL 的**实际执行时间**超过 `long_query_time` 设置的值（默认 10 秒），MySQL 就会把这条 SQL 写到日志文件中。

## 怎么工作

```
请求进来 → MySQL 执行 → 计时
                        ↓ 超过 long_query_time？
                        ↓ YES
                        写入 slow_query_log_file
```}

关键参数：

| 参数 | 含义 | 建议值 |
|------|------|--------|
| `slow_query_log` | 开关 | ON |
| `long_query_time` | 阈值（秒） | 0.1-2（生产环境 1s，开发环境 0.1s） |
| `slow_query_log_file` | 日志文件路径 | 看磁盘空间 |
| `log_queries_not_using_indexes` | 记录没用索引的查询 | ON（谨慎，可能产生大量日志） |
| `min_examined_row_limit` | 至少扫描多少行才记录 | 1000（过滤掉扫几行的"伪慢查询"） |
| `log_slow_admin_statements` | 记录 DDL 慢语句 | ON |

MySQL 还会记录：`Query_time`（总耗时）、`Lock_time`（锁等待时间）、`Rows_sent`（返回行数）、`Rows_examined`（扫描行数）——扫描行数远大于返回行数就是优化重点。

## 怎么用

```sql
-- 查看慢查询是否开启
SHOW VARIABLES LIKE 'slow_query_log';
SHOW VARIABLES LIKE 'long_query_time';

-- 开启慢查询（生产环境建议配置文件里设，这里演示）
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 1;        -- 超过 1 秒就算慢
SET GLOBAL log_queries_not_using_indexes = ON;
SET GLOBAL min_examined_row_limit = 1000;

-- 查看慢查询日志文件位置
SHOW VARIABLES LIKE 'slow_query_log_file';

-- 查看当前慢查询数量
SHOW GLOBAL STATUS LIKE 'Slow_queries';
```

### 分析工具

```bash
# mysqldumpslow（MySQL 自带）
# 按查询时间排序，取最慢的 10 条
mysqldumpslow -s t -t 10 /var/log/mysql/slow.log

# 按出现次数排序（最频繁的慢查询）
mysqldumpslow -s c -t 10 /var/log/mysql/slow.log

# pt-query-digest（Percona Toolkit，更专业）
pt-query-digest /var/log/mysql/slow.log > report.txt
```

## 注意事项

1. **生产环境 `long_query_time` 不要设太小**——0.01 秒会把几乎所有查询都记录下来，日志爆炸，反而影响性能。
2. **`log_queries_not_using_indexes` 要谨慎**——很多小表（几十行）全表扫也很快，没必要加索引。配合 `min_examined_row_limit` 使用。
3. **慢查询日志文件会一直增大**——需要定期清理或用日志轮转（logrotate）。

## 和什么有关

- [EXPLAIN 执行计划](../explain/) —— 发现慢查询后用 EXPLAIN 分析
- [SQL 优化](../sql-optimization/) —— 分析完后怎么优化
- [配置调优](../config-tuning/) —— 有些慢查询是配置问题导致的
