# 代码示例

## 示例 1：基本事务

```sql
BEGIN;
UPDATE account SET balance = balance - 100 WHERE name = '张三';
UPDATE account SET balance = balance + 100 WHERE name = '李四';
COMMIT;
```

## 示例 2：回滚

```sql
BEGIN;
DELETE FROM user WHERE id = 1;
-- 发现删错了！
ROLLBACK;
SELECT * FROM user WHERE id = 1;  -- 数据还在
```

## 示例 3：Savepoint

```sql
BEGIN;
UPDATE account SET balance = balance - 100 WHERE name = '张三';
SAVEPOINT sp1;
UPDATE account SET balance = balance + 100 WHERE name = '李四';
-- 发现转错了
ROLLBACK TO SAVEPOINT sp1;
-- 张三的钱扣了，李四没收——可以重新转
COMMIT;
```
