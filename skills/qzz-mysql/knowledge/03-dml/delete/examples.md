# 代码示例

## 示例 1：删一行

```sql
-- 先 SELECT 确认
SELECT * FROM user WHERE id = 1;

-- 确认无误
DELETE FROM user WHERE id = 1;

-- 返回：Query OK, 1 row affected
```sql

## 示例 2：DELETE vs TRUNCATE

```sql
-- 建测试表
CREATE TABLE test (id INT AUTO_INCREMENT PRIMARY KEY);
INSERT INTO test VALUES (), (), ();  -- 3 行，最后一个 id=3

-- DELETE 不重置自增
DELETE FROM test;
INSERT INTO test VALUES ();  -- id = 4

-- TRUNCATE 重置自增
TRUNCATE TABLE test;
INSERT INTO test VALUES ();  -- id = 1
```sql

## 示例 3：分批删除

```sql
-- 每次删 1000 行，直到 affected rows = 0
DELETE FROM logs WHERE created_at < '2024-01-01' LIMIT 1000;
```sql

循环执行，每次锁定一小批。大表归档时比一次 DELETE 全表安全得多。
