# 代码示例

## 示例 1：当前时间

```sql
SELECT NOW(), CURDATE(), CURTIME();
-- 2025-07-25 14:30:00, 2025-07-25, 14:30:00
```sql

## 示例 2：取年月日

```sql
SELECT YEAR(created_at), MONTH(created_at), DAY(created_at) FROM user;
```sql

## 示例 3：格式化

```sql
SELECT DATE_FORMAT(NOW(), '%Y年%m月%d日 %H:%i');
SELECT DATE_FORMAT(created_at, '%Y-%m') AS month FROM user;
```sql

## 示例 4：计算时间差和加减

```sql
SELECT DATEDIFF(NOW(), '2025-01-01') AS days_from_new_year;
SELECT DATE_ADD(NOW(), INTERVAL 7 DAY) AS next_week;
SELECT DATE_SUB(NOW(), INTERVAL 1 MONTH) AS last_month;
```sql

## 示例 5：正确的日期过滤（走索引）

```sql
-- ❌ WHERE DATE(created_at) = '2025-07-25'  -- 索引失效
-- ✅
SELECT * FROM orders
WHERE created_at >= '2025-07-25' AND created_at < '2025-07-26';
```
