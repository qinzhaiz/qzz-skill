# 代码示例

## 示例 1：配置主从复制（基础步骤）

```sql
-- === 1. 主库：创建复制账号 ===
CREATE USER 'repl'@'%' IDENTIFIED BY 'Repl@123456';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;

-- 查看主库 binlog 位置
SHOW MASTER STATUS;
-- +------------------+----------+--------------+------------------+
-- | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
-- +------------------+----------+--------------+------------------+
-- | mysql-bin.000003 |      123 |              |                  |
-- +------------------+----------+--------------+------------------+

-- === 2. 从库：配置连接到主库 ===
CHANGE MASTER TO
  MASTER_HOST = '192.168.1.100',
  MASTER_PORT = 3306,
  MASTER_USER = 'repl',
  MASTER_PASSWORD = 'Repl@123456',
  MASTER_LOG_FILE = 'mysql-bin.000003',
  MASTER_LOG_POS = 123;

START SLAVE;

-- 查看从库复制状态
SHOW SLAVE STATUS\G
```

关键检查项：
```text
Slave_IO_Running: Yes      ← 必须为 Yes
Slave_SQL_Running: Yes     ← 必须为 Yes
Seconds_Behind_Master: 0   ← 延迟秒数
Last_IO_Error:             ← 错误信息（如果是空说明没问题）
Last_SQL_Error:            ← 错误信息
```

## 示例 2：GTID 方式的复制配置

```sql
-- 主库和从库都需要配置 GTID（my.cnf）
-- gtid_mode = ON
-- enforce_gtid_consistency = ON
-- log_slave_updates = ON    # 从库也要记录 binlog

-- 从库用 GTID 方式连接（不需要指定 File 和 Position！）
CHANGE MASTER TO
  MASTER_HOST = '192.168.1.100',
  MASTER_USER = 'repl',
  MASTER_PASSWORD = 'Repl@123456',
  MASTER_AUTO_POSITION = 1;  -- 自动使用 GTID 定位

START SLAVE;

-- 查看已应用的 GTID
SELECT @@gtid_executed;
```

## 示例 3：主从切换

```sql
-- 场景：主库挂了，需要把从库提升为新主库

-- 在新主库（原从库）上：
STOP SLAVE;
RESET SLAVE ALL;
SET GLOBAL read_only = OFF;
SET GLOBAL super_read_only = OFF;

-- 其他从库：指向新主库
STOP SLAVE;
CHANGE MASTER TO
  MASTER_HOST = '新主库IP',
  MASTER_AUTO_POSITION = 1;  -- 如果用 GTID
START SLAVE;

-- 验证
SHOW SLAVE STATUS\G
-- 检查 Slave_IO_Running 和 Slave_SQL_Running
```
