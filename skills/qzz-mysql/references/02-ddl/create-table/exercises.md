# 练习

## 基础练习

1. 在 `mysql_practice` 库里建一张 `student` 表，至少包含 id（主键）、name、age、major 四列。

2. 用 `DESC student` 查看表结构，确认每一列的类型和约束。

3. 用 `SHOW CREATE TABLE student` 查看完整建表语句，找出 MySQL 帮你补充了哪些你没写的默认值。

## 进阶练习

1. 建表时故意不加主键，用 `SHOW CREATE TABLE` 看看 MySQL 做了什么。

2. 建一张叫 `order` 的表——你会发现报错了。查一下为什么，然后想想实际项目中怎么处理保留字表名。

## 答案

1. 无标准答案。

2. `order` 是 SQL 保留字（ORDER BY）。如果必须用这个表名，用反引号包裹：`` `order` ``。但更好的做法是避免保留字——用 `orders` 或 `t_order`。
