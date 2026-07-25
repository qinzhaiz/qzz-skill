# 代码示例

## 示例 1：查看表的主键

```sql
SHOW CREATE TABLE user\G
-- PRIMARY KEY (`id`) ← 聚簇索引
```

## 示例 2：判断是否回表

```sql
EXPLAIN SELECT * FROM user WHERE name = '张三';
-- Extra: 无 Using index → 回表了

EXPLAIN SELECT name, id FROM user WHERE name = '张三';
-- Extra: Using index → 没回表（二级索引叶子有 id）
```

## 示例 3：UUID vs 自增主键的页分裂

```sql
-- 自增主键：一直往 B+Tree 尾部追加 → 无页分裂
INSERT INTO user (name) VALUES ('张三');  -- id=1, 最后一行
INSERT INTO user (name) VALUES ('李四');  -- id=2, 追加

-- UUID 主键：随机分布在 B+Tree 中 → 页分裂
INSERT INTO user_pk_uuid (id, name) VALUES (UUID(), '张三');  -- 可能在中间某页
```
