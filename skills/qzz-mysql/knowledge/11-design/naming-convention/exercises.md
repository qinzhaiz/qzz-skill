# 练习

## 基础练习

1. 指出以下表名中哪些不合适，并给出修正：
   `Users`, `T_ORDER`, `productList`, `_temp`, `order-detail`

2. 写出一条规范的 CREATE TABLE 语句，包含主键、一个唯一索引、一个联合索引、一个外键。

## 进阶练习

1. 团队里有 10 个开发人员，如何确保每个人都遵守统一的命名规范？列出可行的方案。

## 答案

1. 修正：`Users` → `user`（单数小写），`T_ORDER` → `orders`（去掉前缀），`productList` → `product`（不用驼峰），`_temp` → `temp_data`（不下划线开头），`order-detail` → `order_detail`（不用连字符，用下划线）。

2. 参考：`user` 表带 `username`（UK）、`(status, created_at)` 联合索引、`creator_id` 外键引用自身或另一张表。

3. 方案：(1) 团队文档写明规范 + 提供模板，(2) 用 CI 工具检查（如 sql-lint），(3) Code Review 时检查 DDL 变更，(4) 用 ORM 的 migration 工具统一生成表结构（避免手写 SQL 导致风格差异）。
