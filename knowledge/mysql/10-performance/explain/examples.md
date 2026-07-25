# 代码示例

## 示例 1：对比有索引 vs 无索引

**场景**：相同的查询，加索引前和加索引后的 EXPLAIN 输出。

```sql
-- 无索引（name 列没有索引）
EXPLAIN SELECT * FROM user WHERE name = 'zhangsan';
-- type: ALL（全表扫描）
-- key: NULL
-- rows: 100000
-- Extra: Using where

-- 加了索引后
CREATE INDEX idx_name ON user(name);
EXPLAIN SELECT * FROM user WHERE name = 'zhangsan';
-- type: ref（索引等值查询）
-- key: idx_name
-- rows: 1
-- Extra: NULL
```

**解释**：type 从 ALL 变成 ref，扫描行数从 10 万变成 1——这就是一个索引带来的改变。

## 示例 2：Extra 列速查

```sql
-- ✅ 理想：覆盖索引
EXPLAIN SELECT id, name FROM user WHERE name = 'zhangsan';
-- 假设有索引 idx_name(name)，Extra: Using index
-- 主键在索引的叶子节点中，所以 id 也在索引里

-- ⚠️ 需要关注：文件排序
EXPLAIN SELECT * FROM user ORDER BY created_at LIMIT 10;
-- 假设 created_at 没有索引：Extra: Using filesort
-- 数据库需要把数据读到内存再排序

-- ⚠️ 需要关注：临时表
EXPLAIN SELECT dept, COUNT(*) FROM user GROUP BY dept;
-- dept 没索引：Extra: Using temporary; Using filesort
-- GROUP BY 需要建临时表来聚合

-- ✅ 索引优化后
CREATE INDEX idx_dept ON user(dept);
EXPLAIN SELECT dept, COUNT(*) FROM user GROUP BY dept;
-- Extra: Using index（覆盖索引 + 索引顺序天然支持 GROUP BY）
```

## 示例 3：EXPLAIN ANALYZE 的实际输出

```sql
EXPLAIN ANALYZE SELECT * FROM user
JOIN orders ON user.id = orders.user_id
WHERE user.name = 'zhangsan';
```

```text
-> Nested loop inner join
    -> Index lookup on user using idx_name (name='zhangsan')
        (cost=0.35 rows=1) (actual time=0.012..0.013 rows=1 loops=1)
    -> Index lookup on orders using idx_user_id (user_id=user.id)
        (cost=0.28 rows=3) (actual time=0.008..0.011 rows=3 loops=1)
```

**解读**：
- 用了 Nested Loop Join（驱动表 user，被驱动表 orders）
- user 表通过 idx_name 找到 1 行（预估 1 行，实际 1 行）
- orders 表通过 idx_user_id 找到 3 行（预估 3 行，实际 3 行）
- 预估和实际很接近 → 统计信息准确
