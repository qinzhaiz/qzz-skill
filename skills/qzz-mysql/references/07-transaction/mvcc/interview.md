# 面试题

## Q1：MVCC 是怎么实现的？

**考点**：最高频的 InnoDB 面试题之一。

**回答**：三个关键——隐藏列（DB_TRX_ID + DB_ROLL_PTR）、undo log 版本链、ReadView。每行数据存了最后修改它的事务 ID 和回滚指针。回滚指针串联 undo log 中的历史版本。读数据时 InnoDB 创建 ReadView——根据事务 ID 判断这行对当前事务是否可见。不可见就沿版本链往前找。

### Q2：RC 和 RR 在 MVCC 上的关键区别？

**考点**：不是背定义，是理解 ReadView 的创建时机。

**回答**：RC 每次 SELECT 都创建新的 ReadView——所以能看到别的事务刚提交的修改（不可重复读）。RR 在事务第一次 SELECT 时创建 ReadView，整个事务复用——不管别人提交了什么，你看到的数据版本始终不变（可重复读）。区别就这一处——ReadView 是复用还是重建。
