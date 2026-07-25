# 面试题

## Q1：redo log 和 binlog 有什么区别？

**考点**：最高频的 MySQL 日志面试题。

**回答**：四个维度对比——(1) 所属：redo log 是 InnoDB 引擎层的，binlog 是 MySQL Server 层的（所有引擎共用），(2) 格式：redo log 是物理日志（记录在哪个数据页的哪个偏移量做了什么修改），binlog 是逻辑日志（记录 SQL 语句或行变更），(3) 写入方式：redo log 循环写（固定大小，写满覆盖），binlog 追加写（文件写满后切新文件），(4) 用途：redo log 用于崩溃恢复（crash-safe），binlog 用于主从复制和基于时间点恢复。

**加分点**：能说出为什么需要两个日志——redo log 是 InnoDB 独有的，如果只用 binlog，InnoDB 崩溃了没有日志可以恢复。如果只用 redo log，主从复制和 flashback 做不到。

## Q2：WAL 是什么？为什么 InnoDB 用这个技术？

**考点**：理解设计思想，不只是背定义。

**回答**：WAL（Write-Ahead Logging）就是**先写日志再写数据**。InnoDB 修改数据时，先把修改记录到 redo log（顺序写，极快），然后返回客户端成功。真正的数据页在后台慢慢刷到磁盘。核心原因是性能——顺序写 redo log 比随机写数据页快 1-2 个数量级。如果在 redo log 写完之前崩溃，这个修改本身就丢了（事务没提交），不影响一致性。

**加分点**：能说出崩溃恢复的流程——从 checkpoint 开始重放 redo log，即使事务未提交也先恢复（前滚），然后用 undo log 回滚未提交的事务（回滚）。这是"前滚+回滚"的两阶段恢复。

## Q3：什么时候 redo log 里的数据会被删除/覆盖？

**考点**：理解 checkpoint 机制。

**回答**：redo log 是循环写的，不会"删除"，只会"覆盖"。覆盖的前提是：对应的脏页已经从内存写回了磁盘（checkpoint 之后）。此时即使覆盖了 redo log 中的旧记录，崩溃时也不需要重放它们——因为数据已经在磁盘上了。如果 redo log 写满了但脏页还没刷完，InnoDB 会暂停一切操作，全力刷脏页，直到 checkpoint 推进、腾出空间。
