# 代码示例

## 示例 1：升序和降序

```sql
-- 默认升序
SELECT name, age FROM user ORDER BY age;

-- 降序
SELECT name, age FROM user ORDER BY age DESC;
```sql

## 示例 2：多列排序

```sql
SELECT name, city, age FROM user ORDER BY city ASC, age DESC;
```sql

先按城市字母序排，同城市的按年龄从大到小排。

## 示例 3：分页

```sql
-- 第 1 页（每页 5 条）
SELECT * FROM user ORDER BY id LIMIT 5 OFFSET 0;

-- 第 2 页
SELECT * FROM user ORDER BY id LIMIT 5 OFFSET 5;

-- 最新 10 条
SELECT * FROM user ORDER BY created_at DESC LIMIT 10;
```sql

## 示例 4：游标分页

```sql
-- 不用 OFFSET，用上一页最后一条的 id
SELECT * FROM user WHERE id > 15 ORDER BY id LIMIT 5;
```sql

无论翻到第几页，速度一样快。前提是 id 有序（自增主键）。
