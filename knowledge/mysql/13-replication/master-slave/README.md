# 主从复制

> 一台主库写入，多台从库复制——MySQL 最基础的高可用和数据冗余方案。

## 为什么需要它

一台 MySQL 扛不住所有流量怎么办？不能一直靠"升级配置"解决——单机总有上限。主从复制解决三个问题：
1. **读写分离**：主库处理写，从库分担读，水平扩展读能力
2. **数据冗余**：主库挂了，从库还有一份完整数据
3. **备份与分析**：在从库做备份和数据分析，不影响主库性能

## 它是什么

主从复制（Master-Slave Replication）是 MySQL 内置的数据同步机制：主库上的所有数据变更（INSERT/UPDATE/DELETE）自动同步到从库。核心依赖是 **binlog**（二进制日志）。

```
主库（Master）                    从库（Slave）
     │                                │
     │ 写入                           │
     ↓                                │
  binlog ──── 网络传输 ────→    relay log
                                    │
                                    ↓
                               重放 SQL（数据同步）
```

## 怎么工作

三个线程协作完成：

| 线程 | 在哪个库 | 干什么 |
|------|---------|--------|
| **Binlog Dump 线程** | 主库 | 把 binlog 中的变更发给从库 |
| **IO 线程** | 从库 | 接收 binlog，写入从库的 relay log |
| **SQL 线程** | 从库 | 读取 relay log，重放 SQL，应用变更 |

### 复制过程

1. 从库执行 `CHANGE MASTER TO` 指定主库的连接信息
2. 从库 IO 线程连接主库，请求从某个 binlog 位置开始同步
3. 主库 Binlog Dump 线程把该位置之后的 binlog 推送给从库
4. 从库 IO 线程接收写入 relay log
5. 从库 SQL 线程读取 relay log 重放

### 复制格式

binlog 有三种格式，影响复制行为：

| 格式 | 记录方式 | 优点 | 缺点 |
|------|---------|------|------|
| **STATEMENT** | 记 SQL 语句 | 日志量小 | 某些函数（NOW()、UUID()）在主从不一致 |
| **ROW**（推荐） | 记每一行的变更 | 数据绝对一致 | 日志量大（大事务可能产生大量 binlog） |
| **MIXED** | 通常 STATEMENT，不确定时 ROW | 折中 | 不够纯粹的 ROW 方案 |

**生产环境用 ROW 格式**。

### GTID（全局事务 ID）

MySQL 5.6+ 引入 GTID，给每个事务分配全局唯一 ID。相比传统的"binlog 文件名 + 位置"方式：

- ✅ 切换主库时不需要手动找位点
- ✅ 主从一致性检查更方便
- ✅ 故障恢复更自动化

## 怎么用

```sql
-- === 主库配置 (my.cnf) ===
-- server-id = 1           # 唯一 ID
-- log_bin = mysql-bin     # 开启 binlog
-- binlog_format = ROW     # 推荐 ROW 格式

-- 主库创建复制用户
CREATE USER 'repl'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';

-- 查看主库状态（记录 File 和 Position）
SHOW MASTER STATUS;

-- === 从库配置 ===
-- server-id = 2  # 唯一 ID（不能和主库相同）

-- 从库配置主库连接
CHANGE MASTER TO
  MASTER_HOST = '192.168.1.1',
  MASTER_USER = 'repl',
  MASTER_PASSWORD = 'password',
  MASTER_LOG_FILE = 'mysql-bin.000001',  -- 从 SHOW MASTER STATUS 获取
  MASTER_LOG_POS = 123;

-- 启动复制
START SLAVE;

-- 查看复制状态
SHOW SLAVE STATUS\G
-- 关注：Slave_IO_Running（YES 才正常）
--       Slave_SQL_Running（YES 才正常）
--       Seconds_Behind_Master（0 表示无延迟）
```

## 注意事项

1. **server-id 必须唯一**——主库和所有从库的 server-id 都不能重复。
2. **从库也会写 binlog**——从库的 binlog 可以让它成为其他从库的主库（级联复制）。
3. **从库意外写入**——从库应该设为只读：`SET GLOBAL read_only = ON`。但 super 用户仍然可以写，用 `super_read_only = ON` 彻底防止。
4. **主库不要长期保留大量 binlog**——用 `expire_logs_days` 设置自动清理。

## 和什么有关

- [binlog / 两阶段提交](../../09-execution/two-phase-commit/) —— binlog 是复制的基础
- [读写分离](../read-write-split/) —— 基于主从复制的架构升级
- [主从延迟](../replication-lag/) —— 复制最常见的运维问题
