# 常见错误

## 错误 1：只看 type，不看 Extra

**症状**：type=ref，觉得没问题，但查询还是很慢。

**原因**：type=ref 只说明走了索引，但 Extra 里的 `Using filesort` 或 `Using temporary` 才是真正的瓶颈。走索引 + 额外排序可能比全表扫描还慢。

**怎么修**：看 EXPLAIN 要三列一起看（type + rows + Extra）。type 好但 rows 大、Extra 有警告，也要优化。

## 错误 2：EXPLAIN 和实际执行结果不一样

**症状**：EXPLAIN 显示只用 10 行，实际执行要 10 秒。

**原因**：EXPLAIN 的 rows 是**估算值**，基于统计信息。如果表数据量变化大但没更新统计，估算可能偏差很大。而且 EXPLAIN 不实际执行，看不到真正的耗时。

**怎么修**：用 `EXPLAIN ANALYZE`（实际执行并测量）。定期执行 `ANALYZE TABLE` 更新统计信息。

## 错误 3：只看单表，忽略 JOIN 的驱动表

**症状**：JOIN 查询很慢，每个表单独查都很快。

**原因**：EXPLAIN 的输出从上往下看——第一行是驱动表，它影响了整个 JOIN 的效率。如果驱动表选错了（大表驱动小表），性能差距巨大。

**怎么修**：看 EXPLAIN 第一行的 rows——如果是大表在驱动小表，用 `STRAIGHT_JOIN` 强制指定驱动表顺序。
