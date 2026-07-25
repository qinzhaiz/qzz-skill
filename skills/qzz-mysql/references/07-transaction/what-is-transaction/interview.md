# 面试题

## Q1：COMMIT 之后能 ROLLBACK 吗？

**考点**：事务的基本行为。

**回答**：不能。COMMIT 让修改永久生效——数据写入了 redo log，其他事务已经能看到修改。唯一"回退"的方式是用备份做时间点恢复。

## Q2：长事务有什么危害？

**考点**：实际生产经验。

**回答**：undo log 无法清理——其他事务需要历史版本，导致 undo log 膨胀。行锁长时间持有——其他写事务被阻塞。主从延迟增大——长事务的 binlog 在 COMMIT 时才写入，从库迟迟收不到。

**加分**：知道怎么查长事务——`SELECT * FROM information_schema.innodb_trx WHERE TIME_TO_SEC(TIMEDIFF(NOW(), trx_started)) > 60;`
