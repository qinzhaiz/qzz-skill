# 练习

## 基础练习

1. 用自己的话解释：为什么 Change Buffer 只对非唯一索引生效？唯一索引为什么不能用？

2. 查 `SHOW ENGINE INNODB STATUS` 中 Change Buffer 的 `merged operations`。如果你的数据库中合并次数很高（如 > 10000），说明什么？

## 进阶练习

1. 设计一个实验：对比有 Change Buffer 和无 Change Buffer 时，插入 10 万行数据（表有 5 个非唯一二级索引）的性能差异。用 `SHOW ENGINE INNODB STATUS` 查看 Change Buffer 的合并行为。

2. 如果你的业务是"用户注册后立刻登录"（写入后 1 秒内就查询），Change Buffer 还有用吗？分析原因。

## 答案

1. 唯一索引在插入前必须读磁盘检查唯一性——既然已经读了磁盘把索引页加载到了 Buffer Pool，就不需要 Change Buffer 了（直接在 Buffer Pool 中修改）。非唯一索引不需要唯一性检查，可以不读磁盘直接暂存修改操作。

2. 合并次数高说明：(a) Change Buffer 在工作——写入的二级索引页后续被访问了，(b) 如果合并操作很多且还在增长，说明写入后不久就有大量查询——可以考虑评估 Change Buffer 是否还有价值，或者表设计是否合理。

3. Change Buffer 在 HDD 下效果明显（随机 IO 很慢），SSD 下差距缩小但仍有收益。实验预期：有 CB → 插入更快（少读磁盘），但首次查询这些数据会稍慢（需要合并）。无 CB → 插入时就把索引页读入了，后续查询更快。

4. 写入后立即查询 → 二级索引页会立即被读入 Buffer Pool → Change Buffer 中的操作几乎立即被合并。Change Buffer 几乎没有减少 IO——它只是把 IO 从"写入时"延迟到了"查询时"。这种情况下 Change Buffer 的收益很小。
