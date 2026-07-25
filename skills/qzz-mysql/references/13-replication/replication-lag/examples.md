# 代码示例

## 示例 1：诊断主从延迟

```sql
-- 从库执行：查看延迟
SHOW SLAVE STATUS\G
```

关键字段：
```text
Seconds_Behind_Master: 0    ← 0 或无延迟
Slave_IO_State: Waiting for master to send event  ← IO 线程正常
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
```

```sql
-- 更详细的延迟信息（并行复制时）
SELECT CHANNEL_NAME,
       COUNT_TRANSACTIONS_NOT_DELETED AS pending_transactions,
       COUNT_TRANSACTIONS_RETRIES AS retries
FROM performance_schema.replication_applier_status
WHERE CHANNEL_NAME = '';
```

## 示例 2：并行复制配置对比

```sql
-- === 单线程（MySQL 5.5 及以前） ===
-- my.cnf:
-- slave_parallel_workers = 0
-- 主库并发 100 个事务 → 从库一个个串行回放 → 延迟越来越大

-- === MySQL 5.7+ 并行复制 ===
-- my.cnf:
-- slave_parallel_workers = 8
-- slave_parallel_type = LOGICAL_CLOCK
-- slave_preserve_commit_order = ON
-- 同一 group commit 的事务可以并行回放

SELECT @@slave_parallel_workers;
-- 如果 > 0 且 Seconds_Behind_Master 仍然很大 → 可能是事务冲突太多，并行效果不佳

-- 查看每个 worker 线程的状态
SELECT * FROM performance_schema.replication_applier_status_by_worker;
-- APPLYING_TRANSACTION: worker 正在工作
-- 如果很多 worker 处于 WAITING_FOR_TRANSACTION_DEPENDENCY → 事务之间有冲突
```

## 示例 3：模拟大事务导致的延迟

```sql
-- 主库执行大事务
BEGIN;
UPDATE large_table SET status = 1 WHERE created_at < '2024-01-01';
-- 更新了 100 万行，事务执行了 30 秒
COMMIT;

-- 从库：立即查看延迟
SHOW SLAVE STATUS\G
-- Seconds_Behind_Master: 30  ← 主库执行了 30 秒，从库也要执行 30 秒
-- 等从库回放完，可能又过了 30 秒
```

**教训**：大事务是主从延迟最大的元凶。拆分大事务为小事务（每次 1000 行）。

## 示例 4：监控脚本

```bash
#!/bin/bash
# 监控主从延迟，超过 10 秒发警报

THRESHOLD=10
LAG=$(mysql -h slave_host -e "SHOW SLAVE STATUS\G" | grep "Seconds_Behind_Master" | awk '{print $2}')

if [ "$LAG" != "NULL" ] && [ "$LAG" -gt "$THRESHOLD" ]; then
    echo "WARNING: Replication lag is ${LAG} seconds!" | \
        mail -s "MySQL Replication Alert" admin@example.com
fi
```
