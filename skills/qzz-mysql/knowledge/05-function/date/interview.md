# 面试题

## Q1：DATETIME 和 TIMESTAMP 的区别？

**考点**：最基础的日期类型选择。

**回答**：DATETIME 范围 1000-9999 年，存进去什么查出来什么，不随时区变化。TIMESTAMP 范围 1970-2038，会自动转 UTC 存储并在读取时转回当前时区。新项目用 DATETIME——范围大、行为可预测。

## Q2：怎么查今天的数据？怎么写能用到索引？

**考点**：日期查询 + 索引优化的结合。

**回答**：`WHERE created_at >= CURDATE() AND created_at < DATE_ADD(CURDATE(), INTERVAL 1 DAY)`。不要用 `WHERE DATE(created_at) = CURDATE()`——函数让索引失效。
