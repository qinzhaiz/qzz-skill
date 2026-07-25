# 练习

## 基础练习

1. 在你的 MySQL 上查看 `innodb_file_per_table` 是否开启。找一张表的 .ibd 文件，观察它的大小。

2. 用 `SHOW ENGINE INNODB STATUS` 查看 Buffer Pool 和后台线程的状态。至少找出三个关键指标并理解其含义。

## 进阶练习

1. InnoDB 的 doublewrite buffer 解决了什么问题？如果没有它，什么场景下会导致数据损坏？

2. 画出 InnoDB 的架构图：内存结构（Buffer Pool + Log Buffer + Change Buffer）、后台线程（Master + IO + Purge + Cleaner）、磁盘结构（表空间 + redo log + undo log），标注数据在读写时的流动方向。

## 答案

1. 独立表空间的 .ibd 文件在 `datadir/database_name/table_name.ibd`。大小随数据增长而增长。

2. `Buffer pool size`（总大小）、`Free buffers`（空闲页数）、`Database pages`（已缓存页数）、`Modified db pages`（脏页数）。脏页多且持续增长 → 检查 `innodb_max_dirty_pages_pct` 设置。

3. doublewrite buffer 防止"部分写"问题。InnoDB 的页大小是 16KB，如果写这 16KB 页时操作系统断电、只写了前 4KB → 这一页数据损坏，且 redo log 无法恢复（redo log 记录的是页内偏移量的修改，需要完整页才能重放）。doublewrite buffer 先顺序写一份完整副本，再随机写到实际位置。启动时如果发现目标页坏了，从 doublewrite buffer 恢复。

4. 查询：SELECT → Buffer Pool → （未命中）磁盘 → Buffer Pool → 返回。更新：UPDATE → Buffer Pool（修改为脏页）→ 写 undo log → 写 redo log buffer → Log Buffer 刷到 redo log 磁盘文件 → Master Thread 异步把脏页刷到 .ibd。
