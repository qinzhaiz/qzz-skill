# InnoDB 架构

> InnoDB 不是一块铁板——它由内存结构、磁盘结构、后台线程三部分组成，各自分工明确。

## 为什么需要它

理解了 InnoDB 的内部架构，才能理解之前学的那些概念是怎么串起来的——Buffer Pool 在哪里？redo log 和 undo log 分别存储在哪？为什么数据库重启后数据不丢？这些问题的答案都在 InnoDB 的架构里。

## 它是什么

InnoDB 的架构分为三层：

```sql
┌─────────────────────────────────────┐
│            内存结构                  │
│  Buffer Pool + Change Buffer        │
│  + Adaptive Hash Index + Log Buffer │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│           后台线程                   │
│  Master Thread + IO Thread          │
│  + Purge Thread + Page Cleaner      │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│            磁盘结构                  │
│  表空间: 系统表空间 + 独立表空间     │
│  + redo log + undo log + binlog     │
│  + doublewrite buffer               │
└─────────────────────────────────────┘
```sql

### 内存结构

| 组件 | 作用 | 相关参数 |
|------|------|---------|
| **Buffer Pool** | 缓存数据页和索引页，InnoDB 最重要的内存区域 | `innodb_buffer_pool_size` |
| **Change Buffer** | 缓存对二级索引的修改，延迟写入以提升性能 | `innodb_change_buffer_max_size` |
| **Adaptive Hash Index** | 对热点数据页自动建立哈希索引，加速等值查询 | `innodb_adaptive_hash_index` |
| **Log Buffer** | redo log 的写缓冲，先写这里再刷盘 | `innodb_log_buffer_size` |

### 磁盘结构

| 组件 | 作用 |
|------|------|
| **系统表空间**（`ibdata1`） | 存 change buffer（MySQL 8.0 中数据字典已移至 `mysql.ibd`，doublewrite buffer 在 8.0.20+ 有独立文件） |
| **独立表空间**（`.ibd`） | 每张表一个文件，存数据和索引 |
| **redo log** | 物理日志，循环写，用于崩溃恢复 |
| **undo 表空间** | 存 undo log，用于回滚和 MVCC |
| **临时表空间** | 存临时表和排序操作 |
| **doublewrite buffer** | 防止页部分写入导致数据损坏 |

## 怎么工作

### 查询的路径
```sql
SELECT → Server 层解析优化 → 调 InnoDB 接口
→ Buffer Pool 中找 → 命中？（返回）
→ 未命中 → 从磁盘 .ibd 文件加载到 Buffer Pool → 返回
```sql

### 更新的路径
```sql
UPDATE → Server 层解析优化 → 调 InnoDB 接口
→ 修改 Buffer Pool 中的数据页（标记为脏页）
→ 写 undo log（准备回滚）
→ 写 redo log buffer → 刷到磁盘 redo log（WAL）
→ 后台线程异步刷脏页到磁盘 .ibd 文件
```sql

## 怎么用

```sql
-- 查看 InnoDB 状态概览
SHOW ENGINE INNODB STATUS\G

-- 查看表空间文件
SELECT * FROM information_schema.innodb_tablespaces;

-- 查看 Buffer Pool 大小和使用情况
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool%';

-- 查看 doublewrite 相关
SHOW GLOBAL STATUS LIKE 'Innodb_dblwr%';
```sql

## 注意事项

1. **系统表空间不要和独立表空间混淆**：`ibdata1` 是共享表空间（InnoDB 启动必须的）。`innodb_file_per_table = ON` 时每张表的数据存独立的 `.ibd` 文件。
2. **doublewrite buffer 是安全机制**：InnoDB 先把脏页写到 doublewrite buffer（顺序写），再写到实际位置（随机写）。如果写一半崩溃，用 doublewrite buffer 恢复。
3. **Adaptive Hash Index 不是万能良药**：等值查询多时有用，范围查询或更新频繁时反而有维护开销。

## 和什么有关

- [Buffer Pool 详解](../buffer-pool/) —— InnoDB 最核心的内存组件
- [Change Buffer](../change-buffer/) —— 二级索引的写优化
- [redo log 和 undo log](../../09-execution/redo-undo-log/) —— 日志系统的完整说明
- [MyISAM vs InnoDB](../myisam-vs-innodb/) —— 两种引擎的架构差异
