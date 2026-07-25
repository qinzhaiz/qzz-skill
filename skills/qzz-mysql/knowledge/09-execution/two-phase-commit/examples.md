# 代码示例

## 示例 1：双 1 配置——最安全也最慢

**场景**：金融系统，绝对不能丢数据。

```sql
-- 查看当前配置
SHOW VARIABLES LIKE 'sync_binlog';
SHOW VARIABLES LIKE 'innodb_flush_log_at_trx_commit';

-- 设置为双 1
SET GLOBAL sync_binlog = 1;
SET GLOBAL innodb_flush_log_at_trx_commit = 1;

-- 每个事务提交时：
-- 1. redo log fsync 到磁盘
-- 2. binlog fsync 到磁盘
-- 任何时刻崩溃，两个日志都不丢 → 恢复时数据一致
```sql

**为什么安全？** 崩溃发生时：
- 如果 binlog 已经写入 → 重启后 redo log 从 prepare 改为 commit
- 如果 binlog 没写入 → 重启后 redo log 回滚

两个日志中任何一个在磁盘上，另一个也一定在（或者能被正确处理）。

## 示例 2：理解"先写 binlog 后写 redo log"的问题

**场景**：为什么顺序不能反过来？为什么必须先 redo log prepare 再 binlog？

```sql
-- 假设顺序是：先写 binlog，再写 redo log
-- 步骤 1：binlog 写入（记录 UPDATE c=c+1 WHERE id=2）
-- 步骤 2：此时崩溃了！（redo log 还没写）

-- 后果：
-- 主库重启：没有 redo log → 主库没有这个修改
-- 从库同步：binlog 里有这个修改 → 从库应用了
-- 结果：主库行数 100，从库行数 101 → 不一致！
```

```sql
-- 再假设反过来：先写 redo log，再写 binlog
-- 步骤 1：redo log 写入
-- 步骤 2：此时崩溃了！（binlog 还没写）

-- 后果：
-- 主库重启：redo log 恢复了这个修改 → 主库有这行
-- 从库同步：binlog 里没有 → 从库没有这个修改
-- 结果：主库行数 101，从库行数 100 → 也不一致！
```sql

**结论**：不管先写哪个，只要崩溃时机不巧，就会不一致。两阶段提交用 prepare/commit 协议解决了这个"两个独立的写入无法原子化"的问题。

## 示例 3：查看 binlog 是否有悬空事务

```sql
-- 查看 binlog 列表
SHOW BINARY LOGS;

-- 查看最近一次 binlog 事件
SHOW BINLOG EVENTS IN 'binlog.000001' LIMIT 10;

-- 查看 binlog 格式（ROW/STATEMENT/MIXED）
SHOW VARIABLES LIKE 'binlog_format';
-- ROW 格式最安全，记录每一行的变更
```
