# 面试题

## Q1：什么是索引下推？解决了什么问题？

**考点**：不是背定义，是理解它改变了什么。

**回答**：索引下推（ICP）是 MySQL 5.6 引入的优化，把 WHERE 条件中包含索引列的过滤逻辑下推到存储引擎层执行。以联合索引 `(name, age)` 和查询 `WHERE name LIKE '张%' AND age = 18` 为例：没有 ICP 时，存储引擎把所有 name 匹配的行都回表，返回完整数据给 Server 层，Server 层再过滤 age。ICP 优化后，存储引擎在扫描索引时就检查 age，满足的才回表。核心优化是**减少回表次数**。

**加分点**：能说出 ICP 的约束——只能下推索引列的条件，非索引列仍然需要 Server 层过滤。能区分 ICP 和覆盖索引——ICP 减少回表次数，覆盖索引消除回表。

## Q2：EXPLAIN 中 Extra 列的 `Using index`、`Using index condition`、`Using where` 有什么区别？

**考点**：读懂执行计划，定位性能问题。

**回答**：
- `Using index`：覆盖索引，SELECT 的列全在索引中，不需要回表——最理想。
- `Using index condition`：ICP 生效，WHERE 条件中索引列的部分被下推到存储引擎——较好。
- `Using where`：没有下推，Server 层自己过滤——需要关注。如果同时有索引但出现 `Using where`，说明索引没有被充分利用。
- `Using index; Using where`：覆盖索引 + Server 层过滤——不需要回表但在 Server 层做了额外过滤。

**加分点**：能组合解读——比如 `Using where; Using filesort` 表示既要在 Server 层过滤又要文件排序，是优化重点。
