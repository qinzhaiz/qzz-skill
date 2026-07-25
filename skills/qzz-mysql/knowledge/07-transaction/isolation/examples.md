# 代码示例

## 示例 1：查看隔离级别

```sql
SELECT @@transaction_isolation;
-- REPEATABLE-READ
```sql

## 示例 2：模拟不可重复读（RC 级别下）

```sql
-- 终端 A
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
SELECT age FROM user WHERE id = 1;  -- age = 20

-- 终端 B
UPDATE user SET age = 21 WHERE id = 1;
COMMIT;

-- 终端 A（同一事务）
SELECT age FROM user WHERE id = 1;  -- age = 21 → 不可重复读！
```sql

## 示例 3：RR 级别下的不可重复读消失了

```sql
-- 终端 A
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT age FROM user WHERE id = 1;  -- age = 20

-- 终端 B：修改并提交
UPDATE user SET age = 21 WHERE id = 1;
COMMIT;

-- 终端 A（同一事务）
SELECT age FROM user WHERE id = 1;  -- age = 20 → 可重复读！
```
