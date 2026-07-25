# 主从延迟

> 从库永远比主库慢一点——问题是慢多少、为什么慢、怎么让差距尽量小。

## 为什么需要它

主从复制搞好了、读写分离也上了，然后用户投诉："我刚发的评论怎么刷新就没了？""支付成功了但订单显示待支付？"——这些都是主从延迟导致的。理解延迟的原因和优化方法，是运维 MySQL 的必修课。

## 它是什么

主从延迟（Replication Lag）是主库提交事务到从库完成该事务同步之间的时间差。用 `Seconds_Behind_Master` 来衡量——这个值越大，从库落后得越多。

```sql
主库：tx1 → tx2 → tx3 → tx4 → tx5（最新）
从库：tx1 → tx2 → tx3（还在追）
           ↑ 差了 2 个事务，可能需要几秒
```sql

## 怎么工作

### 延迟的原因

| 原因 | 解释 |
|------|------|
| **大事务** | 主库一个事务执行了 1 秒，从库重放也要 1 秒——但这 1 秒内主库又提交了更多事务 |
| **从库硬件差** | 主库 SSD、从库 HDD → 从库 IO 速度跟不上 |
| **从库有其他负载** | 从库还要处理大量读请求，CPU/IO 被分摊 |
| **单线程回放** | MySQL 5.6 之前从库 SQL 线程只有一个，主库多线程并发写 → 从库串行回放 → 追不上 |
| **网络延迟** | 主从之间网络不稳定或带宽不够 |

### 解决方案

**1. 并行复制（MySQL 5.6+ / 5.7+ / 8.0）**

```sql
主库多线程并发写入
    ↓
binlog 中包含 group commit 信息
    ↓
从库多个 SQL 线程并行回放（slave_parallel_workers）
```sql

MySQL 8.0 的并行复制基于 writeset——分析事务修改的行是否冲突，不冲突就可以并行回放。

```sql
SET GLOBAL slave_parallel_workers = 8;      -- 8 个并行回放线程
SET GLOBAL slave_parallel_type = LOGICAL_CLOCK;  -- 基于组提交的并行
```sql

**2. 半同步复制（Semi-Synchronous Replication）**

异步复制的问题：主库提交后不等从库确认——如果主库宕机，从库可能丢失最后几个事务。半同步复制：主库提交后等待**至少一个**从库确认收到了 binlog（不等待回放完成），才返回客户端成功。

```sql
异步：主库提交 → 不管从库有没有收到 → 返回客户端
半同步：主库提交 → 等待至少 1 个从库确认"收到了" → 返回客户端
```sql

半同步不会消除延迟，但保证了**数据不会丢失**——主库宕机时，至少有一个从库有最新的 binlog。

**3. 级联复制减压**

主库 → 2-3 台中继从库 → 其他从库从中继从库同步。主库只需要维护 2-3 个 binlog dump 连接，而不是 20 个。

### 怎么监控

```sql
SHOW SLAVE STATUS\G
-- Seconds_Behind_Master：主从延迟秒数（NULL 表示复制异常或停止）
```

```sql
-- 更准确的延迟监控（performance_schema）
SELECT THREAD_ID,
       PROCESSLIST_TIME,
       PROCESSLIST_INFO
FROM performance_schema.threads
WHERE NAME = 'thread/sql/slave_worker';
```sql

## 怎么用

```sql
-- 查看当前主从延迟
SHOW SLAVE STATUS\G

-- 开启并行复制
SET GLOBAL slave_parallel_workers = 8;
SET GLOBAL slave_parallel_type = LOGICAL_CLOCK;

-- 查看并行复制状态
SELECT * FROM performance_schema.replication_applier_status_by_worker;

-- 安装半同步插件
-- 主库
INSTALL PLUGIN rpl_semi_sync_master SONAME 'semisync_master.so';
SET GLOBAL rpl_semi_sync_master_enabled = ON;
-- 从库
INSTALL PLUGIN rpl_semi_sync_slave SONAME 'semisync_slave.so';
SET GLOBAL rpl_semi_sync_slave_enabled = ON;
-- 从库需要重启 IO 线程生效
STOP SLAVE IO_THREAD; START SLAVE IO_THREAD;
```sql

## 注意事项

1. **`Seconds_Behind_Master` 是估算值，不是精确值**：它是从库当前时间戳和 binlog 事件时间戳的差值。如果主库服务器时间不同步，这个值不准确。
2. **并行复制不是万能**——依赖事务间的冲突程度。如果大部分事务修改同一行（热点行），并行不起作用。
3. **半同步会降低主库写入性能**——每次 COMMIT 都要等从库确认。在低网络延迟环境下影响较小。

## 和什么有关

- [主从复制](../master-slave/) —— 延迟产生的基础原理
- [读写分离](../read-write-split/) —— 延迟对读操作的影响
- [两阶段提交](../../09-execution/two-phase-commit/) —— binlog 的写入流程
