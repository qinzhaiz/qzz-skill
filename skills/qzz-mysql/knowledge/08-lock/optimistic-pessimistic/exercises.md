# 练习

## 基础练习

1. 建一张有 `version` 列的表，分别在两个终端试试：先读 version → 一个终端更新 + 提交 → 另一个终端再更新。第二个终端更新成功了吗？检查 `affected_rows`。

2. 用 FOR UPDATE 实现一个"选课名额"功能：课程表有 `capacity`（容量）和 `enrolled`（已选人数），写一段 SQL 确保 enrolled 不超过 capacity。

## 进阶练习

1. 比较三种库存扣减方式：裸 UPDATE、FOR UPDATE、乐观锁。各自在什么场景下会出问题？

2. 乐观锁能不能用"时间戳"代替"版本号"？什么时候可以，什么时候不行？

## 答案

1. 第二个终端的 `affected_rows = 0`——因为另一个终端已经把 version 从 1 改成 2 了，第二个终端的 `WHERE version = 1` 不再满足。

2. 选课扣名额：
```sql
BEGIN;
SELECT capacity, enrolled FROM course WHERE id = 1 FOR UPDATE;
-- 应用层判断 enrolled < capacity
UPDATE course SET enrolled = enrolled + 1 WHERE id = 1;
COMMIT;
```sql

3. 裸 UPDATE（`UPDATE product SET stock = stock - 1 WHERE stock > 0`）能防超卖但不能后置判断（比如减了以后又因为业务规则要回滚）。FOR UPDATE 最安全但并发度最低。乐观锁并发度最高但要求业务能接受重试。

4. 时间戳可以——`WHERE updated_at = '读到的旧时间'`。但如果时间精度不够（秒级），同一秒内两次更新可能检测不出冲突。版本号（整数自增）更可靠。
