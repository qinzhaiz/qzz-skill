# 练习

## 基础练习

1. 两个终端再现 MVCC：A 查一行，B 修改同一行并 COMMIT，A 再查——A 看到什么？

2. A 在事务中用 FOR UPDATE 再查一次——这次看到什么？为什么和第一次不一样？

## 进阶练习

1. 查 `information_schema.innodb_trx`，看看有没有正在运行的长事务。

## 答案

1. A 看到旧值——RR 级别下 ReadView 在事务开始时创建，后续快照读复用同一个 ReadView。

2. A 看到新值——FOR UPDATE 是当前读，直接读最新提交的数据。这就是快照读和当前读的区别。
