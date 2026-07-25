# 练习

## 基础练习

1. 给你之前建的 `student` 表加一列 `phone VARCHAR(20)`。

2. 把 phone 列的类型改成 `VARCHAR(32)`。

3. 删掉 phone 列。

## 进阶练习

1. 用 ALTER TABLE 一次完成：加 `email VARCHAR(100)`、在 email 上建索引、把 name 的类型从 VARCHAR(32) 改成 VARCHAR(64)。

2. 查一下 `RENAME TABLE` 能不能改名到另一个数据库。试试 `RENAME TABLE test_db.user TO mysql_practice.user`。

## 答案

1-3 无标准答案。

4. 可以。RENAME TABLE 支持跨库移动表——前提是目标库存在且你有权限。这是最快的数据迁移方式之一。
