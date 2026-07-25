# 日期函数

> 在 SQL 里处理日期时间——取当前时间、格式化、算差值。

## 常用函数

| 函数 | 作用 | 示例 |
|------|------|------|
| NOW() | 当前日期时间 | `2025-07-25 14:30:00` |
| CURDATE() | 当前日期 | `2025-07-25` |
| CURTIME() | 当前时间 | `14:30:00` |
| DATE(expr) | 只取日期部分 | `DATE('2025-07-25 14:30:00')` → `2025-07-25` |
| YEAR/MONTH/DAY | 取年月日 | `YEAR(NOW())` → `2025` |
| DATE_FORMAT(d, fmt) | 格式化 | `DATE_FORMAT(NOW(), '%Y年%m月%d日')` |
| DATEDIFF(a, b) | 相差天数 | `DATEDIFF('2025-07-25', '2025-07-20')` → `5` |
| DATE_ADD(d, INTERVAL n unit) | 加时间 | `DATE_ADD(NOW(), INTERVAL 7 DAY)` |
| DATE_SUB(d, INTERVAL n unit) | 减时间 | `DATE_SUB(NOW(), INTERVAL 1 MONTH)` |

## 实际用法

```sql
-- 查今天注册的用户
SELECT * FROM user WHERE DATE(created_at) = CURDATE();

-- 更好的写法（能走索引）
SELECT * FROM user
WHERE created_at >= CURDATE() AND created_at < DATE_ADD(CURDATE(), INTERVAL 1 DAY);

-- 按月统计
SELECT DATE_FORMAT(created_at, '%Y-%m') AS month, COUNT(*)
FROM user GROUP BY month;

-- 最近 7 天
SELECT * FROM orders WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY);
```sql

## 关键原则：别在 WHERE 里对列套函数

```sql
-- ❌ 索引失效
WHERE DATE(created_at) = '2025-07-25'

-- ✅ 走索引
WHERE created_at >= '2025-07-25' AND created_at < '2025-07-26'
```sql

**对列用函数 = 索引失效。** 改写成范围查询。

## 注意事项

- **DATETIME 写入用 `'YYYY-MM-DD HH:MM:SS'` 格式。** 这是唯一没有歧义的格式。
- **TIMESTAMP 有时区自动转换，DATETIME 没有。** 存进去是什么，查出来就是什么。
- **NOW() 在一个 SQL 语句里只会求值一次。** 插入多行时所有行的 `NOW()` 值都一样——是语句开始执行的时间。

## 和什么有关

- [02-ddl/datatypes/](../../02-ddl/datatypes/) — DATE、DATETIME、TIMESTAMP 的区别
