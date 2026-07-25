# 代码示例

## 示例 1：CASE WHEN

```sql
SELECT name, age,
  CASE
    WHEN age < 18 THEN '未成年'
    WHEN age < 30 THEN '青年'
    WHEN age < 60 THEN '中年'
    ELSE '老年'
  END AS age_group
FROM user;
```

## 示例 2：IF 函数

```sql
SELECT name, IF(age >= 18, '成年', '未成年') AS adult FROM user;
```

## 示例 3：IFNULL 兜底

```sql
SELECT name, IFNULL(phone, '未填写') AS phone FROM user;
```

## 示例 4：COALESCE 取第一个非空

```sql
SELECT name, COALESCE(phone, email, '无联系方式') AS contact FROM user;
```

## 示例 5：行转列

```sql
SELECT DATE_FORMAT(created_at, '%Y-%m') AS month,
  SUM(CASE WHEN status=1 THEN 1 ELSE 0 END) AS active,
  SUM(CASE WHEN status=0 THEN 1 ELSE 0 END) AS inactive
FROM user GROUP BY month;
```
