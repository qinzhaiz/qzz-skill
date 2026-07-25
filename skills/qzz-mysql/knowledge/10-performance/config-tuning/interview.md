# 面试题

## Q1：InnoDB 的 Buffer Pool 是什么？为什么要调它？

**考点**：不只是背参数，要理解它为什么是核心。

**回答**：Buffer Pool 是 InnoDB 的内存缓存区，用来缓存数据页和索引页。查询时先在 Buffer Pool 中找，找到直接返回（微秒级），找不到才读磁盘（毫秒级，慢 100+ 倍）。它是 InnoDB 最重要的性能参数。默认配得很小（128MB），而现代服务器通常有几十 GB 内存。建议设为物理内存的 50-70%。

**加分点**：能说出 Buffer Pool 的 LRU 淘汰策略——最近最少使用的页先被淘汰。能解释命中率怎么看和 99% 的标准。

## Q2：`innodb_flush_log_at_trx_commit` 和 `sync_binlog` 怎么配？

**考点**：性能 vs 安全的权衡。

**回答**：双 1 配置（两个参数都设为 1）最安全——每次事务提交两个日志都刷盘，崩溃不丢数据。但每次 COMMIT 两次 fsync，对写入密集场景性能影响大。如果对数据一致性要求没那么高（日志统计、非关键数据），可以用 `innodb_flush_log_at_trx_commit = 2`（redo log 写 OS 缓存，MySQL 崩溃不丢，OS 崩溃丢 1s）+ `sync_binlog = 1`。绝对不建议两个都设成 0。

**加分点**：能说出组提交（group commit）优化了双 1 配置的 fsync 瓶颈——多个事务的 binlog 合并成一次磁盘写入。
