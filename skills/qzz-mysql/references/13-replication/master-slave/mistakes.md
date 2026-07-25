# 常见错误

## 错误 1：主从 server-id 重复

**症状**：START SLAVE 后，`Slave_IO_Running` 一直是 NO，报错 "server-id must be different"。

**原因**：主库和从库的 `server-id` 配置相同。MySQL 依赖 server-id 来区分不同实例，复制环中不能有重复 ID。

**怎么修**：在 my.cnf 中给每台机器分配唯一 ID。主库和每个从库都要不同。`server_id = 1`（主库），`server_id = 2, 3, 4...`（从库）。改完后重启 MySQL。

## 错误 2：忘记给从库设 read_only

**症状**：应用代码写错了配置，连到了从库执行了写操作。主从数据不一致了，修复起来很痛苦。

**原因**：从库默认没有写保护。任何有权限的连接都可以在从库执行 INSERT/UPDATE/DELETE。

**怎么修**：`SET GLOBAL read_only = ON`（普通用户不可写，super 用户仍可写），`SET GLOBAL super_read_only = ON`（super 用户也不可写）。在 my.cnf 中持久化这些设置。

## 错误 3：用 STATEMENT 格式导致主从数据不一致

**症状**：主库和从库同一张表的数据对不上——某些行的值差了一点点。

**原因**：STATEMENT 格式下，含有非确定性函数的 SQL（如 `NOW()`、`UUID()`、`RAND()`）在主库和从库执行时产生不同的值。`UPDATE t SET code = UUID()` 在主库和从库生成了不同的 UUID。

**怎么修**：用 ROW 格式：`binlog_format = ROW`。ROW 记录的是每一行的实际变更值，不存在"重放时结果不同"的问题。
