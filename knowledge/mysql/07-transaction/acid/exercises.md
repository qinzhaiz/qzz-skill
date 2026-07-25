# 练习

## 基础练习

1. 用事务模拟转账：扣 A 100 → 加 B 100 → COMMIT。验证两边余额正确。

2. 同一个操作但在中途 ROLLBACK——验证两边余额都没有变化。

## 进阶练习

1. 试一下 MyISAM 表：`CREATE TABLE t (id INT) ENGINE=MyISAM;` 写入 BEGIN...ROLLBACK——回滚有用吗？

## 答案

1-2 无标准答案。

3. MyISAM 不支持事务——无论你写不写 ROLLBACK，数据都会立刻持久化。`BEGIN` 和 `ROLLBACK` 在 MyISAM 上无效。
