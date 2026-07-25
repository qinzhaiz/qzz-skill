# 面试题

## Q1：Change Buffer 是什么？解决了什么问题？

**考点**：理解 IO 优化的核心思想。

**回答**：Change Buffer 是 InnoDB 的一种写入优化——对**非唯一二级索引**的修改操作暂存在内存（Buffer Pool 的一部分），延迟合并到磁盘。解决的问题是：多索引表的写入会导致大量随机 IO（每个二级索引都要写磁盘的不同位置）。Change Buffer 把多次随机写合并成更少的批量写，大幅提升写入性能。MySQL 5.5 前叫 Insert Buffer，后来扩展支持 UPDATE 和 DELETE，改名 Change Buffer。

**加分点**：能说出适用条件——(1) 非唯一二级索引，(2) 写入密集，(3) 写入后不会立即查询。能说出 SSD 时代收益降低但未完全消失。

## Q2：Change Buffer 和 redo log 有什么区别？

**考点**：区分两个容易混淆的概念。

**回答**：两个完全不同的东西。Change Buffer 是对**二级索引写操作**的缓存优化——暂存修改操作，延迟写入。redo log 是**所有修改操作**的持久性保证——事务提交必须写 redo log。Change Buffer 的数据在内存中，重启丢失（会从磁盘上的 Change Buffer 页恢复一部分）；redo log 在磁盘上，崩溃恢复的核心。Change Buffer 有自己的 redo log——Change Buffer 中的修改也会记 redo log，保证崩溃后 Change Buffer 中的操作不丢失。

**加分点**：能说出 Change Buffer 的数据也受 redo log 保护——崩溃恢复时，Change Buffer 中的操作通过 redo log 恢复，然后正常合并。
