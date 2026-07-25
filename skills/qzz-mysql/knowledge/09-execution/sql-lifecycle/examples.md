# 代码示例

## 示例 1：用 EXPLAIN 看执行计划

**场景**：想知道优化器打算怎么执行这条 SQL。

```sql
EXPLAIN SELECT * FROM user WHERE id = 1;
```

```text
+----+-------------+-------+-------+---------+-------+------+-------+
| id | select_type | table | type  | key     | ref   | rows | Extra |
+----+-------------+-------+-------+---------+-------+------+-------+
|  1 | SIMPLE      | user  | const | PRIMARY | const |    1 |       |
+----+-------------+-------+-------+---------+-------+------+-------+
```sql

**解释**：`type=const` 表示用了主键等值查询（最快的），`key=PRIMARY` 表示走了主键索引，`rows=1` 表示预估扫描 1 行。

## 示例 2：用 optimizer_trace 看决策细节

**场景**：想知道优化器为什么选了索引 A 而不是索引 B。

```sql
-- 开启 optimizer trace
SET optimizer_trace = 'enabled=on';

-- 执行查询
SELECT * FROM user WHERE name = 'zhangsan' AND age > 20;

-- 查看优化器怎么评估每个索引的代价
SELECT trace FROM information_schema.optimizer_trace\G

-- 关闭（生产环境不要长期开着）
SET optimizer_trace = 'enabled=off';
```sql

**解释**：`trace` 字段是 JSON，包含 `"considered_execution_plans"`——你可以看到优化器考虑了哪些索引，每个的 IO/CPU 代价分别是多少，最终选了哪个。

## 示例 3：观察连接超时

```sql
-- 查看当前连接的空闲超时时间
SHOW VARIABLES LIKE 'wait_timeout';     -- 非交互连接，默认 28800（8小时）
SHOW VARIABLES LIKE 'interactive_timeout';  -- 交互连接

-- 查看当前连接已空闲了多久
SELECT id, user, host, command, time
FROM information_schema.processlist
WHERE command = 'Sleep';
```
