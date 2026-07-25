# 代码示例

## 示例 1：查看和计算 Buffer Pool 命中率

**场景**：判断 `innodb_buffer_pool_size` 是否够大。

```sql
-- 查看当前配置
SELECT @@innodb_buffer_pool_size / 1024 / 1024 / 1024 AS size_gb;

-- 查看命中率相关指标
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read%';
```

```text
+---------------------------------------+-----------+
| Variable_name                         | Value     |
+---------------------------------------+-----------+
| Innodb_buffer_pool_read_requests      | 987654321 |  ← 内存读取次数
| Innodb_buffer_pool_reads              | 1234567   |  ← 磁盘读取次数
+---------------------------------------+-----------+
```sql

**计算**：命中率 = 1 - (1234567 / 987654321) = 99.87% → 很健康

如果命中率低于 99%，说明 Buffer Pool 太小，很多请求需要读磁盘。

## 示例 2：检查 redo log 是否需要调大

```sql
-- 查看 redo log 大小
SHOW VARIABLES LIKE 'innodb_log_file_size';

-- 查看是否有 redo log 等待
SHOW GLOBAL STATUS LIKE 'Innodb_log_waits';
-- > 0 说明 redo log 太小，数据来不及刷到磁盘，log 先满了

-- 查看 InnoDB 的日志状态（在输出的 LOG 部分）
SHOW ENGINE INNODB STATUS\G
```sql

**解读**：如果 `Innodb_log_waits` 持续增长 → redo log 经常写满 → 需要增大 `innodb_log_file_size`。

## 示例 3：配置建议速查

```sql
-- === 内存 ===
-- 专用 MySQL 服务器，物理内存 32GB
SET GLOBAL innodb_buffer_pool_size = 21474836480;  -- 20GB (~65%)

-- SSD 服务器
SET GLOBAL innodb_io_capacity = 5000;      -- SSD 有较高 IOPS
SET GLOBAL innodb_io_capacity_max = 10000;

-- HDD 服务器
SET GLOBAL innodb_io_capacity = 200;       -- HDD 就这点能耐

-- === 连接 ===
SET GLOBAL max_connections = 500;

-- === 表打开缓存 ===
SET GLOBAL table_open_cache = 2000;

-- === 临时表大小 ===
SET GLOBAL tmp_table_size = 67108864;  -- 64MB
SET GLOBAL max_heap_table_size = 67108864;

-- === 查看所有 InnoDB 相关配置 ===
SHOW VARIABLES LIKE 'innodb%';
```
