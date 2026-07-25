# 代码示例

## 示例 1：redo log 刷盘策略对比

**场景**：不同 `innodb_flush_log_at_trx_commit` 设置的差异。

```sql
-- 查看当前设置
SHOW VARIABLES LIKE 'innodb_flush_log_at_trx_commit';
-- 值：0, 1, 或 2

-- 设置为最安全（默认，推荐）
SET GLOBAL innodb_flush_log_at_trx_commit = 1;
-- 每次 COMMIT 都把 redo log buffer 刷到磁盘
-- 性能：★★★ | 安全：★★★★★

-- 折中方案
SET GLOBAL innodb_flush_log_at_trx_commit = 2;
-- 每次 COMMIT 写 redo log 到 OS 缓存，OS 每秒刷盘
-- 性能：★★★★ | 安全：★★★★（MySQL 崩溃不丢，OS 崩溃丢 1s）

-- 最不安全（测试环境可以用）
SET GLOBAL innodb_flush_log_at_trx_commit = 0;
-- 每秒把 redo log buffer 刷到磁盘（不是每次 COMMIT）
-- 性能：★★★★★ | 安全：★★（可能丢 1s 数据）
```

## 示例 2：观察 undo log 膨胀

**场景**：长事务导致 undo log 无法清理。

```sql
-- 终端 A：开启长事务
BEGIN;
UPDATE user SET age = age + 1 WHERE id = 1;
-- 不 COMMIT，保留 MVCC 需要的旧版本

-- 终端 B：更新同一行多次（生成更多 undo log）
UPDATE user SET age = 20 WHERE id = 1;
COMMIT;
UPDATE user SET age = 21 WHERE id = 1;
COMMIT;
UPDATE user SET age = 22 WHERE id = 1;
COMMIT;

-- 查看 InnoDB 状态中的 history list length
SHOW ENGINE INNODB STATUS\G
-- 找到 "History list length"
-- 这个值越大，表示有越多的 undo log 版本等待清理

-- 终端 A 提交，undo log 可以被清理
COMMIT;
-- 再次查看，history list length 应该下降

-- 查看当前活跃的长事务
SELECT trx_id, trx_started,
  TIME_TO_SEC(TIMEDIFF(NOW(), trx_started)) AS secs_running,
  trx_mysql_thread_id
FROM information_schema.innodb_trx
ORDER BY trx_started;
```

## 示例 3：查看 redo log 配置

```sql
-- redo log 总大小
SHOW VARIABLES LIKE 'innodb_log_file%';

-- 查看 redo log 写入量
SHOW GLOBAL STATUS LIKE 'innodb_os_log_written';
-- 累计写入量（字节），可以用这个算写入速率
```
