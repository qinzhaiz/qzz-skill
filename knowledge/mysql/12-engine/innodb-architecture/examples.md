# 代码示例

## 示例 1：查看 InnoDB 架构相关信息

```sql
-- 查看表空间类型（独立表空间是否开启）
SHOW VARIABLES LIKE 'innodb_file_per_table';
-- ON: 每张表独立 .ibd 文件（推荐）
-- OFF: 所有表存在共享表空间 ibdata1

-- 查看所有 InnoDB 表空间
SELECT name, space_type, file_size / 1024 / 1024 AS size_mb
FROM information_schema.innodb_tablespaces
ORDER BY file_size DESC
LIMIT 10;

-- 查看 doublewrite buffer 写入情况
SHOW GLOBAL STATUS LIKE '%dblwr%';

-- 查看 Adaptive Hash Index 状态
SHOW GLOBAL STATUS LIKE 'Innodb_adaptive_hash%';

-- 查看 Log Buffer 大小
SHOW VARIABLES LIKE 'innodb_log_buffer_size';
```

## 示例 2：独立表空间 vs 共享表空间

```sql
-- 共享表空间模式（innodb_file_per_table = OFF）
-- 所有表数据存在 ibdata1 中
-- 问题 1：ibdata1 只增不减（删除表空间不回收）
-- 问题 2：无法单独备份某张表

-- 独立表空间模式（innodb_file_per_table = ON，默认）
-- 每张表数据存在 database/table.ibd 中
-- ✅ 删除表后磁盘空间回收
-- ✅ 可以把 .ibd 文件复制到另一个 MySQL 实例
-- 生产环境务必保持 ON
```

## 示例 3：InnoDB 后台线程

```sql
-- 查看 InnoDB 状态（包含线程信息）
SHOW ENGINE INNODB STATUS\G
```

关键输出解读：

```text
---
BACKGROUND THREAD
---
srv_master_thread loops: 123456  -- Master 线程循环次数
srv_master_thread log flush and writes: 12345  -- 刷日志次数

---
SEMAPHORES
---
-- 如果有大量的信号量等待，说明并发竞争严重

---
FILE I/O
---
-- IO 线程的读写次数、Pending 数量
-- 如果 Pending reads/writes 持续很高，磁盘 IO 可能是瓶颈
```
