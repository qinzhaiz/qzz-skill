# 常见错误

## 错误 1：怕丢数据，把 redo log 设得巨大

**症状**：`innodb_log_file_size` 设了几十 GB，崩溃恢复时数据库十几分钟起不来。

**原因**：redo log 越大 → checkpoint 间隔越长 → 崩溃时 redo log 中需要重放的数据越多 → 恢复时间越长。redo log 不是"缓存"而是"恢复日志"，过大反而有害。

**怎么修**：redo log 总大小设为 1-4 倍 `innodb_buffer_pool_size` 的 25% 左右。比如 buffer pool 8GB，redo log 总共 2-8GB 即可。监控 `SHOW ENGINE INNODB STATUS` 中 redo log 的等待次数。

## 错误 2：为了性能把 `innodb_flush_log_at_trx_commit` 设为 0

**症状**：数据库突然挂了，重启后发现最后一秒的订单数据丢了。

**原因**：设为 0 时，redo log 每秒刷一次而不是每次 COMMIT 刷。如果 MySQL 在这 1 秒内崩溃，还没刷盘的 redo log 记录丢失——已提交的事务也丢了。

**怎么修**：金融、交易场景必须用 1。对数据一致性没那么敏感的场景（日志、埋点、缓存）可以用 2。0 只适合测试环境。

## 错误 3：长事务导致 undo 表空间爆炸

**症状**：磁盘使用率持续增长，`ibdata1` 或 undo 表空间文件越来越大。

**原因**：InnoDB 用 undo log 实现 MVCC。如果有长事务一直不提交，它需要的那个旧版本就不能被 purge 线程清理。后续的更新又不断生成新版本 → 版本链越来越长。

**怎么修**：监控并杀掉长事务。设置 `max_execution_time` 限制单 SQL 执行时间。监控 `information_schema.innodb_trx` 中运行超过 60 秒的事务。
