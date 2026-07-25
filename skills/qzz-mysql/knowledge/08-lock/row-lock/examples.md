# 代码示例

## 示例 1：同一行冲突，不同行并行

```sql
-- 终端 A
BEGIN;
UPDATE user SET age = 21 WHERE id = 1;  -- 持有 id=1 的 X 锁

-- 终端 B
UPDATE user SET age = 22 WHERE id = 1;  -- ❌ 阻塞，同一行
UPDATE user SET age = 22 WHERE id = 2;  -- ✅ 不阻塞，不同行
```sql

**解释**：行锁按行加锁。id=1 和 id=2 是两行，互不影响。这就是行锁比表锁并发度高的原因。

## 示例 2：FOR UPDATE 的阻塞效果

```sql
-- 创建测试表
CREATE TABLE test_lock (id INT PRIMARY KEY, val INT);
INSERT INTO test_lock VALUES (1, 100), (5, 500), (10, 1000);

-- 终端 A
BEGIN;
SELECT * FROM test_lock WHERE id = 5 FOR UPDATE;  -- 持有 id=5 的 X 锁

-- 终端 B 尝试：
UPDATE test_lock SET val = 600 WHERE id = 5;  -- ❌ 阻塞（等 A 提交）
INSERT INTO test_lock VALUES (3, 300);        -- ❌ 也阻塞！（间隙锁防插入）
INSERT INTO test_lock VALUES (7, 700);        -- ❌ 也阻塞！
INSERT INTO test_lock VALUES (11, 1100);      -- ✅ 不阻塞（在范围外）

-- 终端 A
COMMIT;
-- B 的阻塞操作立即执行
```sql

**解释**：RR 级别下 `FOR UPDATE` 加的是 Next-Key Lock，锁住 `(1, 5]` 的整段区间。所以 id=3（在 1~5 之间）和 id=7（在 5~10 之间）都能插入。

等等——id=7 为什么也阻塞？因为 Next-Key Lock 的范围是 `(1, 5]` 和 `(5, 10]`，`WHERE id=5` 实际上锁了 `(1, 5]` 这个区间。但如果需要锁多个区间，取决于具体查询。在这个简单示例中，只有 `(1,5]` 被锁。id=7 不会被阻塞，id=3 和 id=5 会。实际操作中，`WHERE id = 5` 唯一索引等值查询会退化为 Record Lock。对于非唯一索引或范围查询，才会触发 Next-Key Lock 的范围锁。

**修正版本**（明确触发间隙锁）：

```sql
-- 终端 A
BEGIN;
SELECT * FROM test_lock WHERE id > 3 AND id < 8 FOR UPDATE;

-- 终端 B：
INSERT INTO test_lock VALUES (4, 400);   -- ❌ 阻塞（在间隙中）
INSERT INTO test_lock VALUES (2, 200);   -- ✅ 不阻塞
INSERT INTO test_lock VALUES (9, 900);   -- ✅ 不阻塞
```sql

## 示例 3：没索引导致锁全表

```sql
-- user 表的 name 列没有索引
-- 终端 A
BEGIN;
SELECT * FROM user WHERE name = 'zhangsan' FOR UPDATE;

-- 终端 B
INSERT INTO user (name) VALUES ('lisi');  -- ❌ 阻塞！明明不是同一行
UPDATE user SET name = 'wangwu' WHERE id = 999;  -- ❌ 也阻塞！
```sql

**解释**：name 没有索引 → 全表扫描 → 扫描到的每一行都加 X 锁 → 等于锁全表。这就是"没走索引等于表锁"的原因。
