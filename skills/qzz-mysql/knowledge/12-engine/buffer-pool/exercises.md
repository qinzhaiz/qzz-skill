# 练习

## 基础练习

1. 在你的 MySQL 上查看 Buffer Pool 命中率。执行几条全表扫描大表的语句后再次查看，命中率有变化吗？

2. 解释为什么 InnoDB 要把 LRU 分成"热端"和"冷端"。如果不用分代 LRU，全表扫描会带来什么问题？

## 进阶练习

1. 用 `information_schema.innodb_buffer_page` 分析 Buffer Pool 中都缓存了哪些表的哪些页。写一条 SQL 统计每张表在 Buffer Pool 中的占用大小。

2. 设计一个实验：比较 Buffer Pool 大小分别为 128MB 和 2GB 时的查询速度差异。用命中率数据支撑结论。

## 答案

1. 全表扫描大表后命中率可能降低——扫描的冷数据进入了 LRU 冷端，如果数据量超过 Buffer Pool 大小，可能会挤掉部分热点数据。但如果 InnoDB 的分代 LRU 工作正常，影响应该有限。

2. 普通 LRU 中全表扫描的页一旦被访问就放到链表头部，如果扫描的页超过 Buffer Pool 大小，热点数据全被挤出。分代 LRU 把新页放在冷端头部，热点数据在热端。全表扫描的页在冷端很快被淘汰，不会影响到热端的真正热点。

3. 按表分组统计 `information_schema.innodb_buffer_page`：
```sql
SELECT table_name, COUNT(*) * 16 / 1024 AS mb
FROM information_schema.innodb_buffer_page
WHERE table_name IS NOT NULL
GROUP BY table_name ORDER BY mb DESC;
```sql

4. 128MB Buffer Pool 下大表查询命中率低（频繁读磁盘），2GB 下命中率高（大部分数据在内存）。差距随数据量增大而显著。
