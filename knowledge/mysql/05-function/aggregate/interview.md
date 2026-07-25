# 面试题

## Q1：COUNT(*) 和 COUNT(1) 哪个更快？

**考点**：经典误区。

**回答**：一样快。MySQL 优化器会把 COUNT(1) 转换成和 COUNT(*) 相同的执行计划——都是统计行数。网上说的"COUNT(1) 更快"是古老的误区，在现代 MySQL 中不成立。

## Q2：为什么 InnoDB 的 COUNT(*) 比 MyISAM 慢？

**考点**：理解存储引擎差异。

**回答**：MyISAM 维护了一个变量记录总行数，所以 `SELECT COUNT(*) FROM t` 是 O(1)。InnoDB 因为 MVCC——不同事务看到的数据版本不同，无法维护单一计数——必须扫描索引来数行。这是 InnoDB 提供事务隔离性的代价。
