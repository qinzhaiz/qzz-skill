# 代码示例

## 示例 1：拼接

```sql
SELECT CONCAT(name, ' - ', city) AS info FROM user;
SELECT CONCAT_WS('-', province, city, district) AS addr FROM address;
```sql

## 示例 2：截取和替换

```sql
SELECT SUBSTRING(phone, 8, 4) AS last4 FROM user;
SELECT REPLACE(title, 'MySQL', 'MariaDB') FROM post;
```sql

## 示例 3：大小写和去空格

```sql
SELECT UPPER(name), LOWER(city), TRIM(input) FROM form_data;
```sql

## 示例 4：LENGTH vs CHAR_LENGTH

```sql
SELECT name, LENGTH(name), CHAR_LENGTH(name) FROM user;
-- 'MySQL'    → LENGTH=5,  CHAR_LENGTH=5
-- '张三分'   → LENGTH=9,  CHAR_LENGTH=3
```
