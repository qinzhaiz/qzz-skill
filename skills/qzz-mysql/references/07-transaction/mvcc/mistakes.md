# 常见错误

## 错误 1：以为 MVCC 能防所有并发问题

**症状**：用了 RR 隔离级别，但并发更新时仍然出了不一致。

**原因**：MVCC 防的是"读"的并发问题——不可重复读。对于"写"的冲突——同一行被两个事务同时更新——MVCC 不管，要用锁来处理。

**怎么修**：写入冲突用悲观锁（FOR UPDATE）或乐观锁（版本号/CAS）解决。MVCC + 锁 = InnoDB 的并发控制完整方案。

## 错误 2：长事务导致 undo log 膨胀

**症状**：磁盘使用率持续上升，`ibdata1` 文件越来越大。

**原因**：长事务的 ReadView 一直存在——undo log 中旧版本无法被 purge 线程清理。

**怎么修**：监控长事务（innodb_trx 表），拆分大事务为小事务。`SHOW ENGINE INNODB STATUS` 看 history list length。
