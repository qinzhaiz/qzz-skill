# 面试题

## Q1：EXPLAIN 的 type 列从好到差怎么排？

**考点**：面试高频题，必须背下来。

**回答**：`system > const > eq_ref > ref > range > index > ALL`。const 是主键或唯一索引等值查（最多 1 行）。eq_ref 是 JOIN 时被驱动表用主键或唯一键关联。ref 是普通索引等值查。range 是索引范围扫描（`>`、`<`、`BETWEEN`）。index 是扫全索引（比全表好一点）。ALL 是全表扫（需要优化）。

**加分点**：能说出每种 type 的典型场景。能讲出 index 和 ALL 的区别——index 只扫索引树（通常比表小），ALL 扫整张表。

## Q2：Extra 中的 `Using filesort` 为什么不好？怎么优化？

**考点**：理解 filesort ≠ 一定用文件。

**回答**：filesort 并不一定用磁盘文件——如果排序数据量小，在内存中就能完成。但它表示 MySQL 无法用索引天然有序性，需要额外排序操作。优化的关键在于：**让排序列也走索引**。如果 `WHERE a = 1 ORDER BY b`，建 `(a, b)` 联合索引——a 等值后 b 自然有序。注意：如果 ORDER BY 的列不是索引的最左前缀，或者排序方向不一致（一升一降），filesort 仍然会出现。

**加分点**：能区分 `Using filesort` 和 `Using temporary`——前者是"需要排序"，后者是"需要临时表做聚合"，后者通常更严重。能说出如何通过 `max_length_for_sort_data` 参数优化 filesort 表现。
