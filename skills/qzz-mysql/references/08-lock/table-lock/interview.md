# 面试题

## Q1：MDL 是什么？什么时候会出现 MDL 等待？

**考点**：理解自动锁机制，不是背命令。

**回答**：MDL（Metadata Lock）是 MySQL 5.5 引入的元数据锁，用来防止 DML 和 DDL 同时操作同一张表。执行 SELECT/INSERT/UPDATE/DELETE 自动加 MDL 读锁，执行 ALTER TABLE 等 DDL 自动加 MDL 写锁。读锁之间不互斥，读写锁互斥。MDL 等待的典型场景是：长事务持有 MDL 读锁不释放，DDL 申请 MDL 写锁被阻塞，DDL 后面进来的 DML 也因为排队被阻塞。最终整张表不可用。

**加分点**：能说出 MDL 的公平队列机制——后来的读锁虽然和先来的读锁不互斥，但由于前面有写锁在排队，必须等写锁执行完。能提到通过 `sys.schema_table_lock_waits` 诊断。

## Q2：全局锁和表锁有什么区别？

**考点**：区分不同粒度的表级锁。

**回答**：全局锁（`FLUSH TABLES WITH READ LOCK`）锁的是整个数据库实例，所有库所有表都是只读。通常用于全库备份。表锁（`LOCK TABLES`）锁的是指定的一张或多张表。在 InnoDB 中用得很少，因为 InnoDB 有行锁。mysqldump 的 `--single-transaction` 可以替代全局锁——通过 MVCC 得到一致性快照。

**加分点**：能说出 InnoDB 为什么不需要手动表锁——行锁 + MVCC 提供了更好的并发性能。能说清楚 FTWRL 和 `--single-transaction` 各自适用场景。
