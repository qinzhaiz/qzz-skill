# 面试题

## Q1：InnoDB 的 Buffer Pool 怎么管理缓存页？用的什么淘汰策略？

**考点**：不只是"LRU"，要理解 InnoDB 的改进。

**回答**：InnoDB 用**改良的分代 LRU**。链表分为热端（5/8）和冷端（3/8）。新读入的页放到冷端头部，而不是热端。如果冷端的页被再次访问且满足时间条件（在冷端超过 1 秒），升级到热端头部。热端淘汰的页降到冷端。这样设计是为了防止全表扫描污染 Buffer Pool——大表扫描的页进入冷端后很快被淘汰，不会挤走真正热点的数据。

**加分点**：能说出 `innodb_old_blocks_pct`（冷端占比，默认 37%）和 `innodb_old_blocks_time`（升级到热端需要的时间，默认 1000ms）。能说出分代 LRU 的全称和设计目的。

## Q2：什么时候脏页会被刷到磁盘？

**考点**：理解刷盘机制而不是死记硬背。

**回答**：四个触发条件——(1) redo log 快写满了（最紧急），InnoDB 必须推进 checkpoint，刷掉对应区域的脏页，(2) Buffer Pool 空间不够用，淘汰脏页前必须先刷盘，(3) Master Thread 后台定期刷，保证脏页比例不超过 `innodb_max_dirty_pages_pct`（默认 90%），(4) MySQL 正常关闭时全刷。生产环境频繁出现"等待刷盘"的情况说明 IO 能力不足，需要提高 `innodb_io_capacity`。

**加分点**：能说出 `innodb_max_dirty_pages_pct_lwm`（低水位线，默认 10%）和 `innodb_adaptive_flushing`（自适应刷新）——提前开始刷脏页，避免紧急刷盘导致性能抖动。
