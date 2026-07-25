# Buffer Pool 详解

> InnoDB 的心脏——数据库性能的好坏，70% 取决于 Buffer Pool 配置得对不对。

## 为什么需要它

磁盘比内存慢 10 万倍。如果没有缓存，每次查询都要读磁盘——你的数据库每秒只能处理几十个请求。Buffer Pool 用内存缓存热点数据，让大部分请求在微秒级完成。

## 它是什么

Buffer Pool 是 InnoDB 在内存中开辟的一块区域，用来缓存**数据页**和**索引页**。默认大小是 128MB（严重偏小），生产环境通常设为物理内存的 50-70%（通用服务器），MySQL 专用服务器可到 80%。

核心机制：

| 机制 | 作用 |
|------|------|
| **LRU 链表** | 管理哪些页该保留、哪些该淘汰 |
| **Free List** | 记录哪些内存页还没被使用 |
| **Flush List** | 记录哪些页是脏页（已修改未写回磁盘），需要刷盘 |
| **预读** | 预测接下来要访问的页，提前加载到 Buffer Pool |

## 怎么工作

### InnoDB 的 LRU 算法（改良版）

普通 LRU 有个问题：一次全表扫描可能把整个 Buffer Pool 都刷掉（大量冷数据把热点数据挤出去）。InnoDB 用**分代 LRU**——把 LRU 链表分成两段：

```sql
LRU 链表：[ 热端 (5/8) ][ 冷端 (3/8) ]
            ↑ 频繁访问的    ↑ 新加载的放在这里
```sql

新页先放在冷端头部，如果在冷端被访问了足够多次 → 升到热端。全表扫描的页在冷端很快被淘汰，不会污染热端。

### 脏页刷盘（Flush）

修改过的页（脏页）需要写回磁盘，但不需要立即写。InnoDB 有几个刷盘时机：

1. **redo log 快满了**——必须刷，否则无法写入更多 redo log
2. **Buffer Pool 空间不够**——淘汰脏页前必须先刷盘
3. **MySQL 正常关闭**——全部刷盘
4. **后台 Master Thread 定时刷**——平滑刷，避免集中 IO

### 多实例 Buffer Pool

MySQL 5.6+ 支持把 Buffer Pool 拆成多个实例（`innodb_buffer_pool_instances`）。多线程并发访问时，每个线程访问不同的实例，减少内部锁竞争。建议：Buffer Pool < 1GB 就 1 个实例，> 1GB 设置 4-8 个实例。

## 怎么用

```sql
-- 配置（my.cnf）
-- innodb_buffer_pool_size = 20G   # 设为物理内存的 50-70%
-- innodb_buffer_pool_instances = 8 # 大 Buffer Pool 分成多实例

-- 查看 Buffer Pool 命中率
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read%';
-- 命中率 = 1 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests)

-- 查看 Buffer Pool 使用情况
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_pages%';
-- total: 总页数
-- free: 空闲页数（如果长期为 0，可能需要加大）
-- data: 数据页数
-- dirty: 脏页数（如果脏页比例过高，检查 max_dirty_pages_pct 和 IO 能力）

-- 查看 Buffer Pool 预读效率
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read_ahead%';
```sql

## 注意事项

1. **Buffer Pool 不是越大越好**——超过物理内存 80% 可能导致 OS swap（比不缓存还慢）。留足够内存给 OS 和其他进程。
2. **预读可能适得其反**——`innodb_read_ahead_threshold` 控制预读的激进程度。SSD 下预读收益不明显，反而可能加载无用页。
3. **观察脏页比例**——脏页太多说明刷盘跟不上写入速度，可能需要调大 `innodb_io_capacity` 或增加 redo log 大小。

## 和什么有关

- [InnoDB 架构](../innodb-architecture/) —— Buffer Pool 在架构中的位置
- [配置调优](../../10-performance/config-tuning/) —— `innodb_buffer_pool_size` 是第一个要调的参数
- [Change Buffer](../change-buffer/) —— Change Buffer 是 Buffer Pool 的一部分
- [redo log 和 undo log](../../09-execution/redo-undo-log/) —— 脏页刷盘的触发条件
