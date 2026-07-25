# 练习

## 基础练习

1. 在自己的 MySQL 上开启慢查询日志（阈值设 0.1 秒），执行几条故意慢的 SQL（比如全表扫描大表带 ORDER BY），查看慢查询日志文件的内容。

2. 解释慢查询日志中 `Rows_sent` 和 `Rows_examined` 差距巨大的含义。什么情况下这是正常的，什么情况下需要优化？

## 进阶练习

1. 用 `pt-query-digest` 分析慢查询日志，生成报告。找出 Top 3 最耗时的查询模式。

2. 设计一个监控方案：每天自动检查慢查询数量，如果比前一天增加超过 50%，发送告警。

## 答案

1. 慢查询日志会记录 SQL、执行时间、锁等待时间、扫描行数和返回行数。`Rows_examined` 远大于 `Rows_sent` 且执行时间长 → 需要优化索引。

2. `Rows_examined >> Rows_sent` 通常意味着：(1) 没有合适的索引 → 全表扫描后才过滤，(2) LIMIT 大偏移量 → 扫了很多行再丢掉前面。偶尔的报表查询（需要扫大量数据做汇总）是正常的；高频接口查询不正常。

3. `pt-query-digest` 报告会按 `Query_time total` 排序，列出最耗时的查询模式，并给出优化建议（如"97% of the query time was spent on this query"）。

4. 定时采集 `SHOW GLOBAL STATUS LIKE 'Slow_queries'`，记录到监控系统。对比当天和前一天同时段的增量。如果突增，先看慢查询日志找新出现的慢 SQL。
