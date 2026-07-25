# 代码示例

## 示例 1：对比 ICP 开启 vs 关闭

**场景**：联合索引 `(name, age)`，查询 `name LIKE '张%' AND age = 18`。

```sql
-- 建表和数据
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    age INT,
    city VARCHAR(50),
    INDEX idx_name_age (name, age)
);

-- 插入测试数据（大量姓张的，年龄不同）
-- ... 省略批量 INSERT ...

-- 关闭 ICP
SET optimizer_switch = 'index_condition_pushdown=off';
EXPLAIN SELECT * FROM users WHERE name LIKE '张%' AND age = 18;
-- Extra: Using where
-- 存储引擎把所有 name LIKE '张%' 的行都返回给 Server 层

-- 开启 ICP
SET optimizer_switch = 'index_condition_pushdown=on';
EXPLAIN SELECT * FROM users WHERE name LIKE '张%' AND age = 18;
-- Extra: Using index condition
-- 存储引擎在索引层就过滤掉 age != 18 的行
```

## 示例 2：ICP 不能下推的情况

**场景**：索引里没有要过滤的列。

```sql
-- 索引只有 (name)，没有 age
CREATE INDEX idx_name ON users (name);

EXPLAIN SELECT * FROM users WHERE name LIKE '张%' AND age = 18;
-- Extra: Using where（不是 Using index condition）
-- age 不在索引里，ICP 无法下推
```

**解释**：ICP 只能下推**索引列**的过滤条件。age 不在索引中，存储引擎在索引扫描时看不到 age 的值，必须在回表之后才能判断。

## 示例 3：覆盖索引 vs ICP——哪个更好？

```sql
-- 覆盖索引：SELECT 的列全在索引中
CREATE INDEX idx_name_age_city ON users (name, age, city);

EXPLAIN SELECT name, age, city FROM users
WHERE name LIKE '张%' AND age = 18;
-- Extra: Using where; Using index
-- 不需要 ICP——覆盖索引根本不回表，ICP 无用武之地

-- ICP 场景：SELECT 了索引外的列，需要回表
EXPLAIN SELECT * FROM users
WHERE name LIKE '张%' AND age = 18;
-- Extra: Using index condition
-- 需要回表，但 ICP 减少了回表次数
```
