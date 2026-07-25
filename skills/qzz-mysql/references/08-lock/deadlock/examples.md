# 代码示例

## 示例 1：最经典的死锁场景

**场景**：两个事务以不同顺序更新同一组行。

```sql
-- 终端 A
BEGIN;
UPDATE user SET age = 21 WHERE id = 1;  -- 持有 id=1 的 X 锁

-- 终端 B
BEGIN;
UPDATE user SET age = 22 WHERE id = 2;  -- 持有 id=2 的 X 锁

-- 终端 A（继续）
UPDATE user SET age = 23 WHERE id = 2;  -- 等 B 释放 id=2 → 阻塞

-- 终端 B（继续）
UPDATE user SET age = 24 WHERE id = 1;  -- 等 A 释放 id=1 → 死锁！
-- MySQL 返回：ERROR 1213 (40001): Deadlock found when trying to get lock;
-- try restarting transaction
```

**解释**：A 等 B，B 等 A，形成环。InnoDB 检测到后选择回滚 B（修改更少的那个）。终端 A 的 UPDATE id=2 立即成功执行。

## 示例 2：间隙锁引发的死锁

**场景**：INSERT 也会死锁——间隙锁互相等待。

```sql
-- 假设表中已有 id=1 和 id=10 两行

-- 终端 A
BEGIN;
INSERT INTO test (id) VALUES (5);  -- 在 (1,10) 间隙上加锁

-- 终端 B
BEGIN;
INSERT INTO test (id) VALUES (6);  -- 也在 (1,10) 间隙上加锁，但不冲突

-- 终端 A
INSERT INTO test (id) VALUES (7);  -- 等 B 释放……

-- 终端 B
INSERT INTO test (id) VALUES (4);  -- 等 A 释放…… → 死锁！
```

**解释**：插入意向锁虽然不互斥（多个 INSERT 可以同时在不同的位置插入），但当它们互相阻塞时，仍可能死锁。这在高并发 INSERT 场景下很常见。

## 示例 3：查看死锁日志

```sql
SHOW ENGINE INNODB STATUS\G
```

```text
------------------------
LATEST DETECTED DEADLOCK
------------------------
*** (1) TRANSACTION:
UPDATE user SET age = 23 WHERE id = 2
*** (1) HOLDS THE LOCK(S):
RECORD LOCKS ... index PRIMARY of table `test`.`user` ... lock_mode X locks rec
Record lock, heap no 2 PHYSICAL RECORD: id=1

*** (1) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS ... index PRIMARY of table `test`.`user` ... lock_mode X locks rec
Record lock, heap no 3 PHYSICAL RECORD: id=2

*** (2) TRANSACTION:
UPDATE user SET age = 24 WHERE id = 1
*** (2) HOLDS THE LOCK(S):
RECORD LOCKS ... index PRIMARY of table `test`.`user` ... lock_mode X locks rec
Record lock, heap no 3 PHYSICAL RECORD: id=2

*** (2) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS ... index PRIMARY of table `test`.`user` ... lock_mode X locks rec
Record lock, heap no 2 PHYSICAL RECORD: id=1

*** WE ROLL BACK TRANSACTION (2)
```
