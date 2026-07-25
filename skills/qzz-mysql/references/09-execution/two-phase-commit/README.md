# 两阶段提交

> redo log 和 binlog 之间的一致性协议——保证主库崩溃恢复后，数据在主库和从库之间一致。

## 为什么需要它

一个 UPDATE 语句涉及两个日志：InnoDB 的 redo log（用于崩溃恢复）和 Server 层的 binlog（用于主从复制）。如果两个日志的写入不是原子的，崩溃可能发生在其中一个写入完成之后——导致主库用 redo log 恢复了数据，但从库的 binlog 里没有对应记录（主从数据不一致）。

两阶段提交解决了这个问题：**保证 redo log 和 binlog 要么都写成功，要么都不写**。

## 它是什么

两阶段提交（Two-Phase Commit，2PC）是分布式事务的经典协议，MySQL 内部用它来协调 redo log 和 binlog：

```
Phase 1 (Prepare): 写 redo log，状态置为 "prepare"
Phase 2 (Commit):  写 binlog，然后把 redo log 状态改为 "commit"
```

崩溃恢复的判断规则：

| 崩溃时机 | redo log 状态 | binlog 有没有 | 恢复行为 |
|----------|-------------|-------------|---------|
| redo log 写入前崩溃 | 无记录 | 无 | 回滚——事务没发生 |
| redo log prepare 后, binlog 写入前崩溃 | prepare | 无 | **回滚**——binlog 没有，从库不会同步 |
| binlog 写入后, redo log commit 前崩溃 | prepare | 有 | **提交**——binlog 有了，必须保证主从一致 |
| redo log commit 后 | commit | 有 | 已提交，无需处理 |

**核心逻辑**：binlog 写没写决定一切。写了就必须提交（否则主从数据不一致），没写就必须回滚。

## 怎么工作

### UPDATE 完整流程

```
1. 执行器：取 ID=2 的行
2. InnoDB：在 Buffer Pool 中找到或加载数据页
3. 执行器：拿到数据，修改 c = c + 1
4. InnoDB：更新 Buffer Pool 中的数据页（脏页）
5. InnoDB：写 undo log（准备回滚）
6. InnoDB：写 redo log → 状态 prepare（Phase 1 完成）
7. Server 层：写 binlog
8. InnoDB：redo log 状态改为 commit（Phase 2 完成）
```

### 崩溃在准备阶段的处理

MySQL 启动时按顺序扫描 binlog，找到最近一次 binlog 的结束位置。然后检查 redo log：所有 binlog 中有对应记录的事务，redo log 中的记录被提交；没有对应记录的事务，redo log 中的记录被回滚。

## 怎么用

```sql
-- 查看 binlog 刷盘策略
SHOW VARIABLES LIKE 'sync_binlog';
-- 0: 系统决定刷盘时机
-- 1: 每次提交都刷（推荐，保证 binlog 不丢）

-- 查看 redo log 刷盘策略
SHOW VARIABLES LIKE 'innodb_flush_log_at_trx_commit';

-- 双 1 配置（最安全）
-- sync_binlog = 1
-- innodb_flush_log_at_trx_commit = 1
-- 每个事务两个日志都刷盘，一个都不丢

-- 查看 binlog 信息
SHOW MASTER STATUS;
SHOW BINARY LOGS;
```

## 注意事项

1. **双 1 配置影响性能**：每次 COMMIT 都要两次刷盘（redo log + binlog），对写入密集型场景有较大影响。可以考虑用组提交（group commit）优化——多个事务批量刷盘。
2. **MySQL 的组提交优化**：MySQL 5.6+ 引入 binlog 组提交，把多个事务的 binlog 合并成一次 fsync。这也是为什么即使双 1 配置，高并发下性能也不一定差。
3. **分布式 XA 事务**：MySQL 支持跨引擎的 XA 事务（`XA START` / `XA END` / `XA PREPARE` / `XA COMMIT`），但实际生产中很少用——复杂性太高，出错后恢复困难。

## 和什么有关

- [redo log 和 undo log](../redo-undo-log/) —— 两阶段提交的两个参与者
- [事务 ACID](../../07-transaction/acid/) —— 持久性的关键机制
- [主从复制](../../13-replication/what-is-replication/) —— binlog 的用途
