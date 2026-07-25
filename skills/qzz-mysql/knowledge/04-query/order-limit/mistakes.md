# 常见错误

## 错误 1：大偏移量分页

**症状**：翻到第 100 页以后越来越慢。

**原因**：`LIMIT 10 OFFSET 100000` 会扫描并丢弃前面 10 万行。OFFSET 越大越慢。

**怎么修**：用游标分页——`WHERE id > 上一页最后id ORDER BY id LIMIT 10`。但不能跳页。

## 错误 2：ORDER BY 和 LIMIT 忘了配合

**症状**：`SELECT * FROM user LIMIT 10` 每次返回的行不一样。

**原因**：没有 ORDER BY 时，MySQL 返回行的顺序是不确定的——取决于存储引擎和物理存储。

**怎么修**：LIMIT 必须配合 ORDER BY 一起用。分页查询尤其如此。

## 错误 3：NULL 在排序中最前还是最后？

**症状**：升序排列时 NULL 值排在最前面，业务预期是排在最后。

**原因**：MySQL 里 NULL 被认为是最小值。

**怎么修**：`ORDER BY IFNULL(col, '')` 或 `ORDER BY col IS NULL, col`——先把 NULL 排开。
