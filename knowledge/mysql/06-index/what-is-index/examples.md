# 代码示例

## 示例 1：建索引 + 看效果

```sql
-- 建索引前
EXPLAIN SELECT * FROM user WHERE name = '张三';
-- key: NULL → 全表扫

-- 建索引
CREATE INDEX idx_name ON user(name);

-- 建索引后
EXPLAIN SELECT * FROM user WHERE name = '张三';
-- key: idx_name → 走索引了
```

## 示例 2：查看索引

```sql
SHOW INDEX FROM user;
-- 列出所有索引：PRIMARY、idx_name……

SHOW CREATE TABLE user\G
-- 看建表语句里的索引定义
```

## 示例 3：删除索引

```sql
DROP INDEX idx_name ON user;

SHOW INDEX FROM user;
-- idx_name 不在了
```
