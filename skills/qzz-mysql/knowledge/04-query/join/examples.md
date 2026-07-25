# 代码示例

## 示例 1：INNER JOIN

```sql
SELECT u.name, o.amount
FROM user u
INNER JOIN orders o ON u.id = o.user_id;
```sql

只返回有订单的用户。`u` 和 `o` 是表别名。

## 示例 2：LEFT JOIN

```sql
SELECT u.name, o.amount
FROM user u
LEFT JOIN orders o ON u.id = o.user_id;
```sql

所有用户都在——没有订单的用户 amount 显示 NULL。

## 示例 3：多表 JOIN

```sql
SELECT u.name, o.amount, p.name AS product_name
FROM orders o
JOIN user u ON o.user_id = u.id
JOIN product p ON o.product_id = p.id
WHERE o.amount > 100;
```sql

## 示例 4：被驱动表没索引的后果

```sql
-- orders.user_id 没有索引 → 每次关联全表扫 orders
EXPLAIN SELECT * FROM user JOIN orders ON user.id = orders.user_id;
-- type: ALL（全表扫）→ 慢
```
