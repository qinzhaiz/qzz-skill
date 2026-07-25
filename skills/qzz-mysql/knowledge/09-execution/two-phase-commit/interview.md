# 面试题

## Q1：MySQL 为什么要用两阶段提交？

**考点**：不只是背流程，要理解没有 2PC 会怎样。

**回答**：两阶段提交是为了保证 redo log（引擎层，物理日志）和 binlog（Server 层，逻辑日志）的一致性。这两个日志必须同时成功或同时失败，否则主库崩溃恢复后数据就和从库不一致了。如果先写 redo log 后写 binlog→ 崩溃时 binlog 丢失 → 主库有、从库没有。如果先写 binlog 后写 redo log→ 崩溃时 redo log 丢失 → 从库有、主库没有。2PC 通过 redo log 的 prepare/commit 状态解决了这个问题。

**加分点**：能说出崩溃恢复的判断规则——binlog 有没有才是关键。能提到组提交（group commit）优化了双 1 配置下的 fsync 瓶颈。

## Q2：为什么 redo log 写成功了还不能直接提交？

**考点**：理解 prepare 状态的必要性。

**回答**：redo log prepare 之后不能直接提交，因为 binlog 还没写。如果直接提交，binlog 写之前崩溃了，redo log 是 commit 状态（会被恢复），但 binlog 没有记录——主库恢复了这行数据，从库没有，数据不一致。prepare 状态的作用就是给恢复系统一个"先别急，看看 binlog 怎么说"的信号。

**加分点**：能说出恢复时的具体判断——扫描 binlog 最后位置，prepare 状态的事务如果在 binlog 中有对应记录就提交，没有就回滚。
