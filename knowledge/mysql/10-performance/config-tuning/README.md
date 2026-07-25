# 配置调优

> 改几个关键参数，MySQL 性能可能翻倍——从最重要的那个开始。

## 为什么需要它

刚装好的 MySQL 用的是出厂配置，这些配置针对的是几十年前的硬件（假设只有 128MB 内存）。你买的服务器有 32GB 内存，MySQL 可能只用了 128MB——剩下的全浪费了。配置调优就是告诉 MySQL："你有一台更好的机器，大胆用。"

## 它是什么

MySQL 配置调优的核心是**让数据库充分利用硬件资源**。最重要的几个参数：

| 参数 | 作用 | 建议值 |
|------|------|--------|
| `innodb_buffer_pool_size` | InnoDB 的缓存——缓存数据页和索引 | 物理内存的 50%-70% |
| `innodb_log_file_size` | redo log 文件大小 | 1-4GB |
| `innodb_flush_log_at_trx_commit` | redo log 刷盘策略 | 1（安全）或 2（折中） |
| `sync_binlog` | binlog 刷盘策略 | 1（安全） |
| `innodb_io_capacity` | 告诉 InnoDB 磁盘的 IOPS 能力 | SSD: 1000-20000, HDD: 200 |
| `max_connections` | 最大连接数 | 500-1000 |

**最重要的参数是 `innodb_buffer_pool_size`**——它决定了 InnoDB 能缓存多少数据在内存中。设太小 → 频繁读磁盘，设太大 → OS 没内存了还得用 swap（更慢）。

## 怎么工作

### Buffer Pool 为什么是核心

```
查询请求 → Buffer Pool（内存）→ 命中 → 直接返回（微秒级）
                        ↓
                      未命中 → 从磁盘加载 → 返回（毫秒级，慢 100+ 倍）
```

Buffer Pool 越大，命中率越高，磁盘 IO 越少。但 MySQL 并不是有多少用多少——Buffer Pool 不是越大越好：
- 超过物理内存的 80% 时，OS 和别的进程没内存了
- 如果 MySQL 专用服务器，可以设到 70-80%
- 如果是混合用途（和 Web 服务同一台机器），50-60%

### redo log 大小的影响

```
redo log 太小 → 快速写满 → 频繁刷脏页 → 磁盘 IO 飙升 → 卡顿
redo log 太大 → checkpoint 间隔长 → 崩溃恢复慢
```

一般设为 1-4GB。如果 `SHOW ENGINE INNODB STATUS` 里经常出现 `log waits`（redo log 满了在等），就该调大。

## 怎么用

```sql
-- 查看当前 Buffer Pool 大小
SELECT @@innodb_buffer_pool_size / 1024 / 1024 / 1024 AS pool_size_gb;

-- 查看 Buffer Pool 命中率（越高越好，>99% 算正常）
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read%';
-- Innodb_buffer_pool_read_requests = 从 Buffer Pool 读的次数
-- Innodb_buffer_pool_reads = 从磁盘读的次数
-- 命中率 = 1 - (reads / requests)

-- 查看 redo log 是否有等待
SHOW GLOBAL STATUS LIKE 'Innodb_log_waits';
-- > 0 表示 redo log 太小，需要调整

-- 查看当前连接数
SHOW GLOBAL STATUS LIKE 'Threads_connected';
SHOW VARIABLES LIKE 'max_connections';
```

## 注意事项

1. **Buffer Pool 改完需要重启吗？** MySQL 8.0 支持动态调整：`SET GLOBAL innodb_buffer_pool_size = 8G;`（需要先分配足够内存）。
2. **不要一上来就调到 80%**——观察一段时间（至少一两天），看实际 Buffer Pool 使用率和命中率再调整。
3. **redo log 大小需要在配置文件里改**，不能动态调整。修改后需要重启。

## 和什么有关

- [redo log 和 undo log](../../09-execution/redo-undo-log/) —— redo log 参数详解
- [SQL 执行流程](../../09-execution/sql-lifecycle/) —— Buffer Pool 在查询中的作用
- [慢查询日志](../slow-query/) —— 调完配置后用来验证效果
