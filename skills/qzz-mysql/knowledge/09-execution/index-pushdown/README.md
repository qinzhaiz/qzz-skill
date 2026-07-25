# 索引下推（ICP）

> 把 WHERE 过滤条件下推到存储引擎层执行，减少回表次数——MySQL 5.6 引入的重要优化。

## 为什么需要它

假设有联合索引 `(name, age)`，查询条件是 `name LIKE '张%' AND age = 18`。没有 ICP 时：存储引擎把"所有姓张的行"都返回给 Server 层，Server 层再过滤 `age = 18`。问题是——存储引擎回表读了 100 行，实际只需要 5 行。

ICP 优化后：存储引擎在回表之前就检查 `age = 18`，只有两个条件都满足的才回表。回表次数从 100 降到 5。

## 它是什么

ICP（Index Condition Pushdown）是 MySQL 5.6 引入的优化：把一部分 WHERE 条件"下推"到存储引擎层去执行——在**扫描索引时就过滤掉不符合条件的行**，而不是等数据全部返回 Server 层再过滤。

这里有两点关键：
1. **只下推能用索引列判断的条件**——`WHERE` 里能通过索引直接判断的部分
2. **下推发生在存储引擎层**——在回表之前，不满足条件的直接跳过

## 怎么工作

### 没有 ICP 的流程

```sql
存储引擎：扫描联合索引 → 逐行回表取完整行 → 返回给 Server 层
Server 层：拿到完整行 → 检查 age = 18 → 满足的保留
问题：回表了 100 次，实际只需要 5 次
```sql

### 有 ICP 的流程

```sql
存储引擎：扫描联合索引 → 在索引中检查 age = 18 → 满足的才回表 → 返回给 Server 层
Server 层：直接拿结果
好处：只回表了 5 次
```sql

**关键条件**：ICP 只能下推"索引中包含的列"的过滤条件。如果 `age` 不在索引里，ICP 无法下推 `age = 18` 的检查。

## 怎么用

```sql
-- 查看 ICP 是否开启（默认开启）
SHOW VARIABLES LIKE 'optimizer_switch';

-- 用 EXPLAIN 看是否使用了 ICP
EXPLAIN SELECT * FROM user
WHERE name LIKE '张%' AND age = 18;
-- Extra 列：Using index condition → ICP 生效
```sql

`Extra` 列的关键含义：
- `Using index condition`：ICP 生效，WHERE 条件被下推到存储引擎
- `Using where`：没有 ICP，Server 层自己过滤
- `Using index`：覆盖索引，不需要回表

## 注意事项

1. **ICP 默认开启，不需要手动配置**。`optimizer_switch` 中的 `index_condition_pushdown=on`。
2. **覆盖索引不需要 ICP**——如果 SELECT 的列全在索引里，根本不需要回表，ICP 没有用武之地。
3. **ICP 适用于 range、ref、eq_ref、ref_or_null 访问方式**。
4. **ICP 减少的是回表次数**，不是索引扫描行数。索引扫描还是扫了 100 个姓张的，只是回表只回了 5 次。

## 和什么有关

- [索引基础](../../06-index/what-is-index/) —— ICP 依赖联合索引
- [覆盖索引](../../06-index/covering-index/) —— 覆盖索引进一步消除了所有回表
- [SQL 执行流程](../sql-lifecycle/) —— ICP 改变了 Server 层和存储引擎层的分工
