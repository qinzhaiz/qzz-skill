# 代码示例

## 示例 1：单层 CTE

```sql
WITH beijing_users AS (
    SELECT * FROM user WHERE city = '北京'
)
SELECT name, age FROM beijing_users WHERE age > 20;
```

## 示例 2：多个 CTE 串联

```sql
WITH
    big_orders AS (
        SELECT user_id, amount FROM orders WHERE amount > 100
    ),
    top_users AS (
        SELECT user_id, COUNT(*) AS cnt FROM big_orders GROUP BY user_id
    )
SELECT u.name, t.cnt
FROM top_users t JOIN user u ON t.user_id = u.id
ORDER BY t.cnt DESC;
```

## 示例 3：递归 CTE（树形结构）

```sql
WITH RECURSIVE org AS (
    -- 顶层：没有上级的员工
    SELECT id, name, manager_id, 1 AS level
    FROM employee WHERE manager_id IS NULL

    UNION ALL

    -- 下层：上级在 org 里的员工
    SELECT e.id, e.name, e.manager_id, org.level + 1
    FROM employee e JOIN org ON e.manager_id = org.id
)
SELECT * FROM org ORDER BY level, id;
```
