# 代码示例

## 示例 1：原子性——回滚

```sql
BEGIN;
UPDATE account SET balance = balance - 100 WHERE name = '张三';
SELECT balance FROM account WHERE name = '张三';  -- 看到扣了
-- 模拟出错
ROLLBACK;
SELECT balance FROM account WHERE name = '张三';  -- 恢复到原来的值
```sql

## 示例 2：持久性——COMMIT 后重启不丢

```sql
BEGIN;
DELETE FROM user WHERE id = 999;
COMMIT;
-- 即使立刻断电重启，这条数据也不会回来
SELECT * FROM user WHERE id = 999;  -- Empty set
```sql

## 示例 3：查看 autocommit

```sql
SELECT @@autocommit;  -- 1 = ON, 0 = OFF
SET autocommit = 0;   -- 关闭自动提交（所有操作都需要手动 COMMIT）
```
