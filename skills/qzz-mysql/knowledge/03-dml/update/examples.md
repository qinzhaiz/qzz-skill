# 代码示例

## 示例 1：改一行

```sql
-- 先确认
SELECT id, name, city FROM user WHERE id = 1;
-- 输出：id=1, name='张三', city='北京'

-- 再改
UPDATE user SET city = '广州' WHERE id = 1;

-- 验证
SELECT id, name, city FROM user WHERE id = 1;
-- 输出：id=1, name='张三', city='广州'
```sql

## 示例 2：批量更新 + 表达式

```sql
-- 所有 2024 年之前的订单标记为已归档，同时给 archived_at 填上当前时间
UPDATE orders
SET status = 'archived', archived_at = NOW()
WHERE created_at < '2024-01-01';
```sql

## 示例 3：LIMIT 分批更新

```sql
-- 大表不要一次改太多行——分批来
UPDATE logs SET processed = 1 WHERE processed = 0 LIMIT 1000;

-- 反复执行直到 affected rows = 0
```sql

这条在生产环境下很实用：几百万行的表，一次 UPDATE 全表可能锁很久。LIMIT 1000，循环执行，每次锁一小会。
