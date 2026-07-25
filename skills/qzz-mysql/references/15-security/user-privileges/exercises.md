# 练习

## 基础练习

1. 在你的 MySQL 上创建一个新用户，授予对某个数据库的 SELECT 和 INSERT 权限。用这个用户连接并测试：SELECT 成功、DELETE 失败（没有权限）。

2. 用 `SHOW GRANTS` 查看 root 用户和你创建的应用用户的权限差异。

## 进阶练习

1. 模拟一个权限审计：查出哪些用户有 DROP 权限、哪些可以从任意 IP 连接、哪些密码为空。

2. 设计一套多环境（开发/测试/生产）的权限策略。开发环境可以宽松吗？生产环境必须怎么限制？

## 答案

1. 创建 `myapp` 用户并授予 `test_db` 的 SELECT 和 INSERT 权限。尝试 DELETE 会报 `ERROR 1142: DELETE command denied to user 'myapp'@'...' for table '...'`。

2. root 通常有 `ALL PRIVILEGES ON *.* WITH GRANT OPTION`——可以操作所有库、可以把权限给他人。应用用户通常只有特定库的 CRUD 权限。

3. 审计查询：(a) `SELECT user, host FROM mysql.user WHERE Drop_priv = 'Y'`，(b) `WHERE host = '%' AND user NOT IN ('repl')`，(c) `WHERE authentication_string = ''`。

4. 开发环境：可以宽松（root 或 ALL PRIVILEGES），但要和数据真实的安全需求隔离。测试环境：接近生产配置。生产环境：最小权限、限制 IP、强密码策略、不使用 root、每个应用独立账户。
