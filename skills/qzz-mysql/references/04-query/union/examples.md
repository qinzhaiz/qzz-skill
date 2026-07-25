# 代码示例

## 示例 1：合并两个查询

```sql
SELECT name FROM user WHERE city = '北京'
UNION
SELECT name FROM user WHERE city = '上海';
```

## 示例 2：UNION vs UNION ALL

```sql
-- UNION 会自动去重（慢）
SELECT city FROM user UNION SELECT city FROM user_backup;

-- UNION ALL 保留重复（快）
SELECT city FROM user UNION ALL SELECT city FROM user_backup;
```

## 示例 3：合并后排序

```sql
SELECT name, '用户' AS type FROM user WHERE city = '北京'
UNION ALL
SELECT name, '备份' AS type FROM user_backup WHERE city = '北京'
ORDER BY name;
```
