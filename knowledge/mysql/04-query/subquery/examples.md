# 代码示例

## 示例 1：标量子查询

```sql
-- 查出年龄大于平均年龄的用户
SELECT name, age FROM user
WHERE age > (SELECT AVG(age) FROM user);
```

内层返回一个数字，外层用这个数字做过滤。

## 示例 2：IN 子查询

```sql
-- 查出有订单的用户
SELECT * FROM user
WHERE id IN (SELECT DISTINCT user_id FROM orders);
```

内层返回一组 id，外层查这些 id 的用户。

## 示例 3：EXISTS 子查询

```sql
SELECT * FROM user
WHERE EXISTS (
    SELECT 1 FROM orders WHERE orders.user_id = user.id AND amount > 100
);
```

只要子查询有至少一行结果，EXISTS 返回 TRUE。不关心具体值——`SELECT 1` 或 `SELECT *` 都一样。

## 示例 4：NOT IN 的 NULL 陷阱

```sql
-- 子查询包含 NULL → 永远返回空
SELECT * FROM user WHERE id NOT IN (1, 2, NULL);
-- Empty set

-- 安全写法
SELECT * FROM user WHERE id NOT IN (SELECT DISTINCT user_id FROM orders WHERE user_id IS NOT NULL);
-- 或直接用 NOT EXISTS
```
