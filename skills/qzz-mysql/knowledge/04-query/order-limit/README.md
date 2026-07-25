# 排序和分页

> ORDER BY 排顺序。LIMIT 控制返回多少行。两者组合就是"第 N 页"。

## ORDER BY

### 升序和降序

```sql
SELECT * FROM user ORDER BY age;         -- 默认升序（小→大）
SELECT * FROM user ORDER BY age ASC;     -- 明确升序
SELECT * FROM user ORDER BY age DESC;    -- 降序（大→小）
```sql

### 多列排序

```sql
SELECT * FROM user ORDER BY city ASC, age DESC;
```sql

先按城市升序排，城市相同的再按年龄降序排。**排序优先级从左到右**——第一个列相同才看第二个。

### 用别名排序

```sql
SELECT name, age, city FROM user ORDER BY age;
```sql

ORDER BY 可以引用 SELECT 里的列名，也可以引用别名（因为 ORDER BY 在 SELECT 之后执行）。

## LIMIT + OFFSET

### 限制行数

```sql
SELECT * FROM user LIMIT 5;           -- 前 5 行
SELECT * FROM user ORDER BY id DESC LIMIT 10;  -- 最新 10 条
```sql

### 分页

```sql
-- 第 1 页（前 10 条）
SELECT * FROM user ORDER BY id LIMIT 10 OFFSET 0;

-- 第 2 页
SELECT * FROM user ORDER BY id LIMIT 10 OFFSET 10;

-- 第 N 页
SELECT * FROM user ORDER BY id LIMIT 10 OFFSET (N-1)*10;
```sql

## 大偏移量的坑

```sql
SELECT * FROM user ORDER BY id LIMIT 10 OFFSET 100000;
```bash

即使只返回 10 行，MySQL 也要先扫描并丢弃前 10 万行。OFFSET 越大越慢。

### 优化：游标分页

```sql
-- 不用 OFFSET——记住上一页最后一条的 id，从它之后开始
SELECT * FROM user WHERE id > 100000 ORDER BY id LIMIT 10;
```sql

每次都走索引定位到起点，无论翻到第几页速度一样。要求 id 是自增主键。

## 注意事项

- **ORDER BY 默认升序。** DESC 才降序。
- **NULL 在排序中最小还是最大？** MySQL 里 NULL 默认为最小值（升序时排最前面）。
- **大偏移量分页用游标分页。** 不要用 OFFSET + 大数字。

## 和什么有关

- [SELECT 基础](../select-basic/) — SELECT 的完整用法
- [WHERE 条件](../where/) — 先过滤，再排序
- [索引基础](../../06-index/what-is-index/) — 排序列建索引可以跳过 filesort
