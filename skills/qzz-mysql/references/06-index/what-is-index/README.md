# 索引是什么

> 索引是书的目录——让你不用翻遍整本书去找一个词，而是先查目录，直接翻到目标页。

## 为什么需要它

没索引时，查一条数据等于全表扫描——一行一行对，直到找到你想要的。1000 万行的表，查一行平均要扫 500 万行。

加索引后，B+Tree 3-4 层就能定位到目标行——只扫个位数行。

一张表没有任何索引的时候：

```sql
SELECT * FROM user WHERE name = '张三';
-- MySQL 逐行扫描，直到找到所有匹配的行。
-- 100 万行 → 可能扫描 100 万行
```

加了索引后：

```sql
-- 先在你的 name 列上建个索引
CREATE INDEX idx_name ON user(name);

-- 同样的查询，MySQL 直接定位到目标行
SELECT * FROM user WHERE name = '张三';
-- 100 万行 → 可能只扫描 1-3 行
```

## 怎么用

### 创建索引

```sql
CREATE INDEX idx_name ON user(name);
CREATE INDEX idx_city_age ON user(city, age);  -- 联合索引
```

### 查看表上有哪些索引

```sql
SHOW INDEX FROM user;
```

### 删除索引

```sql
DROP INDEX idx_name ON user;
```

### 通过 ALTER TABLE 建索引

```sql
ALTER TABLE user ADD INDEX idx_name(name);
ALTER TABLE user DROP INDEX idx_name;
```

## 怎么判断索引用上了

```sql
EXPLAIN SELECT * FROM user WHERE name = '张三';
```

看 `key` 列：

- 有索引名 → 索引用上了 ✅
- `NULL` → 没走索引 ❌

## 索引的代价

索引不是免费的。每建一个索引：

- **写入变慢**：INSERT / UPDATE / DELETE 时除了更新数据，还要更新索引
- **占用空间**：索引是单独的数据结构，有自己的存储开销

所以**不是越多越好**——建要建值得的。后面 [when-to-use](../when-to-use/) 专门讲。

## 注意事项

- **主键自动有索引。** `PRIMARY KEY` 列自带聚簇索引，不用另外建。
- **外键不会自动建索引。** 必须手动 `CREATE INDEX`。
- **索引名推荐前缀 `idx_`。** 如 `idx_name`、`idx_city_age`，一眼就知道这是索引。

## 和什么有关

- [B+Tree 原理](../btree/) — 索引底层用什么数据结构
- [聚簇索引和二级索引](../clustered-secondary/) — 回表是什么
- [什么时候该建索引](../when-to-use/) — 建索引的黄金法则
