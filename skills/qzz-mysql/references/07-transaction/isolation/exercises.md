# 练习

## 基础练习

1. 把你当前连接的隔离级别从 RR 改为 RC，再改回来。

2. 两个终端分别模拟 RC 和 RR 下的不可重复读——看结果有什么不同。

## 进阶练习

1. RR 级别下，A 事务 SELECT 查到一个范围（比如 city='北京'），B 插入一行 city='北京' 并提交。A 再用 FOR UPDATE 查同范围——会看到新行吗？

## 答案

1. `SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;`

2. RC 下同一事务两次查同一行结果可能不同（不可重复读）。RR 下两次查结果相同（可重复读）。

3. 会——FOR UPDATE 是当前读，不走 MVCC，能看到已提交的数据。这就是 RR 下幻读的残余场景——Next-Key Lock 是用来防这种的。
