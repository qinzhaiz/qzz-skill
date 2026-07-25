# 练习

## 基础练习

1. 用自己的话解释：为什么 redo log 和 binlog 都需要？只有其中一个会发生什么问题？

2. 解释崩溃恢复中 redo log 状态为 "prepare" 时的处理逻辑：怎么决定该提交还是该回滚？

## 进阶练习

1. 画出两阶段提交的完整时序图，标注每个步骤崩溃时恢复系统会怎么处理。

2. 为什么说 `innodb_flush_log_at_trx_commit = 1` + `sync_binlog = 1` 是"最安全"的配置？这个配置下，两阶段提交的哪个步骤可能成为性能瓶颈？

## 答案

1. 只有 redo log——能崩溃恢复，但没法做备份和主从复制。只有 binlog——可以备份复制，但 InnoDB 引擎崩溃无法恢复（binlog 是逻辑日志，不知道数据页内部状态）。

2. MySQL 启动时扫描 binlog，找到最近一次写入的位置。然后遍历 redo log 中状态为 prepare 的事务，每个事务检查 binlog 中是否有对应记录——有就提交，没有就回滚。

3. 两阶段提交的写入路径上，有两个 fsync 操作：redo log fsync（Phase 1→2 之间）和 binlog fsync（Phase 2 之后）。双 1 配置下每个事务两次 fsync，高并发时可能成为瓶颈。MySQL 通过组提交（group commit）缓解这个问题——多个事务共享一次 binlog fsync。

4. 性能瓶颈在 fsync。高并发时，redo log fsync 和 binlog fsync 各一次。MySQL 的组提交通常解决了 binlog fsync 的瓶颈（多个事务合并），但 redo log fsync 仍然逐事务执行。
