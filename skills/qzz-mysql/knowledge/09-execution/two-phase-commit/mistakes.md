# 常见错误

## 错误 1：以为双 1 配置是默认的

**症状**：线上跑了很久，某天机器断电，重启后发现数据对不上。

**原因**：MySQL 默认的 `innodb_flush_log_at_trx_commit` 是 1，但 `sync_binlog` 默认是 1（MySQL 8.0）。在更早版本中 `sync_binlog` 默认是 0——binlog 刷盘由 OS 决定，断电可能丢失。即使 redo log 安全，binlog 不安全也会导致主从数据不一致。

**怎么修**：线上金融系统确认双 1 配置：`innodb_flush_log_at_trx_commit = 1, sync_binlog = 1`。注意这会影响写入性能，需要综合评估。

## 错误 2：分布式 XA 事务用过头

**症状**：经常看到 XA 事务卡在 prepare 状态，重启后数据库需要很长时间恢复。

**原因**：MySQL 的 XA 事务（跨存储引擎的分布式事务）虽然支持，但实际生产中极其容易出错——XA PREPARE 后、XA COMMIT 前如果连接断开了，prepare 状态的事务就永远卡着。重启时需要逐一校验每个 XA 事务。

**怎么修**：不要使用 MySQL 原生的 XA 事务。如果确实需要跨资源的事务一致性，用应用层的 Saga 模式或 TCC 模式。
