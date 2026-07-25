# 常见错误

## 错误 1：Buffer Pool 设成内存的 90%

**症状**：数据库刚开始很快，运行一段时间后越来越慢，最后整个服务器卡死。

**原因**：Buffer Pool 占用了太多内存，OS 没有内存做文件系统缓存，甚至触发 swap——swap 是磁盘速度，一旦 swap 整个系统性能崩溃。

**怎么修**：MySQL 专用服务器设 50-70%，共享服务器设 40-50%。观察 OS 的 `free -h`，确保还有可用内存。如果已经开始 swap，立即调小 Buffer Pool。

## 错误 2：redo log 太小导致频繁卡顿

**症状**：数据库每隔几分钟就卡一下，`SHOW PROCESSLIST` 看到很多 "waiting for handler commit"。

**原因**：redo log 太小，写入密集型场景下很快写满。写满时 InnoDB 必须暂停所有操作，全力把脏页刷到磁盘（checkpoint），直到 log 中腾出空间。

**怎么修**：增大 `innodb_log_file_size`（比如从 128MB 调到 2GB）。调完后重启 MySQL，观察 `Innodb_log_waits` 是否仍增长。

## 错误 3：按"别人推荐的配置"直接抄

**症状**：网上搜了一个 my.cnf 配置，改完重启，数据库表现更差了。

**原因**：每台服务器的硬件、负载、数据量都不同。别人 128GB 内存机器的配置不适合你 4GB 内存的开发机。

**怎么修**：理解每个参数的含义，根据自己的服务器和使用场景调整。先改最重要的几个（Buffer Pool, redo log, IO capacity），再根据监控数据逐步优化。
