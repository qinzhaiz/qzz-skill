# Change Buffer

> 插入数据时，先别急着更新所有索引——把对二级索引的修改暂存起来，等读的时候再合并。

## 为什么需要它

假设你有一张 10 个索引的表。插入一行数据 → 主键索引更新（很快，顺序写）+ 9 个二级索引更新（每个都可能跑到磁盘不同位置，随机写）。每次 INSERT 都是 10 次 IO——随机 IO 是磁盘性能的杀手。

Change Buffer 的思路：**对二级索引的修改先不写入磁盘，暂存在 Change Buffer 中。等需要读这个索引页时再合并。** 这样 10 次随机 IO 变成了 1 次顺序 IO + 9 次可能延迟合并。

## 它是什么

Change Buffer 是 Buffer Pool 的一部分，专门缓存对**非唯一二级索引**的 INSERT/UPDATE/DELETE 操作。当要修改一个二级索引页，而这个页还不在 Buffer Pool 中时——不立即读磁盘，而是把修改操作暂存到 Change Buffer。等未来该页被加载到 Buffer Pool 时，再一次性合并所有待处理的操作。

```
INSERT 一行
    ↓
更新主键索引（立即写入）
    ↓
更新二级索引：这个索引页在 Buffer Pool 中吗？
    ├── 是 → 直接修改（和普通操作一样）
    └── 否 → 把操作存到 Change Buffer，不读磁盘！
                  ↓
        将来该页被加载到 Buffer Pool 时
                  ↓
        合并 Change Buffer 中的所有待处理操作
```

## 怎么工作

### 为什么只对非唯一索引

Change Buffer 只缓存对**非唯一二级索引**的修改。唯一索引需要读磁盘检查唯一性——既然已经读了磁盘，就不需要 Change Buffer 了（直接修改就行）。

### 合并时机

1. **该页被读入 Buffer Pool 时**——执行 SELECT 或 UPDATE 用到了这个索引
2. **Master Thread 定期合并**——后台线程定时执行
3. **MySQL 正常关闭时**——全部合并到磁盘
4. **Change Buffer 快满了**——被动触发合并

### 什么时候有用

- ✅ **写入密集**：大量 INSERT（如日志记录、流水数据）
- ✅ **二级索引多**：表有多个非唯一二级索引
- ✅ **写入后不立即读**：写入的数据要等一段时间才会被查询
- ❌ **唯一索引多**：Change Buffer 不适用
- ❌ **写入后立即读**：刚写就查，所有页本来就在 Buffer Pool 里

## 怎么用

```sql
-- 查看 Change Buffer 状态
SHOW ENGINE INNODB STATUS\G
-- 找到 "INSERT BUFFER AND ADAPTIVE HASH INDEX" 部分

-- 关键指标：
-- Ibuf: size 1（Change Buffer 当前使用的页数）
-- free list len（空闲页数）
-- seg size（段大小）
-- merges（合并次数）
-- merged operations（合并操作数）中的 insert/delete mark/delete

-- 查看 Change Buffer 配置
SHOW VARIABLES LIKE 'innodb_change_buffering';
-- all: 缓存所有操作（insert, delete mark, purge）
-- none: 关闭
-- inserts: 只缓存 insert
-- deletes: 缓存 delete mark
-- changes: insert + delete mark
-- purges: 缓存 purge 操作

-- Change Buffer 最大占比（Buffer Pool 的百分比）
SHOW VARIABLES LIKE 'innodb_change_buffer_max_size';
-- 默认 25（占用 Buffer Pool 最多 25%）
```

## 注意事项

1. **Change Buffer 占用 Buffer Pool 空间**——虽然叫 Buffer，但它和 Buffer Pool 是同一块内存。设得太大 → 挤占了数据缓存。默认 25% 比较合理。
2. **SSD 下收益减少**：HDD 时代 Change Buffer 的收益很大（避免随机 IO），SSD 下随机 IO 也快很多，收益变小但仍然有用。
3. **唯一索引不能利用 Change Buffer**——设计表时如果二级索引全是唯一的，Change Buffer 几乎没有用。

## 和什么有关

- [Buffer Pool 详解](../buffer-pool/) —— Change Buffer 是 Buffer Pool 的一部分
- [索引基础](../../06-index/what-is-index/) —— 二级索引和唯一索引的区别
- [InnoDB 架构](../innodb-architecture/) —— Change Buffer 在架构中的位置
