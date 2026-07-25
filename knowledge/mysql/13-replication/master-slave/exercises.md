# 练习

## 基础练习

1. 在自己的两台 MySQL 实例上（或 Docker 容器）搭建主从复制。用 SHOW SLAVE STATUS 验证复制是否正常。

2. 在主库上执行 CREATE TABLE 和 INSERT，观察从库是否同步了数据。在从库上查询验证。

## 进阶练习

1. 用 Docker Compose 搭建一主两从的复制拓扑。模拟主库宕机，将一个从库提升为新主库，另一个从库重新指向新主库。

2. 对比 STATEMENT 和 ROW 格式的 binlog：分别在两种格式下执行 `UPDATE user SET age = age + 1`，用 `mysqlbinlog` 查看 binlog 内容。

## 答案

1. 关键步骤：主库开 binlog → 创建复制用户 → 记下 binlog 位置 → 从库配置 CHANGE MASTER → START SLAVE。`Slave_IO_Running` 和 `Slave_SQL_Running` 都为 Yes 即正常。

2. 主库操作后从库通过 relay log 重放 SQL 应用变更。如果从库没有同步，检查 SHOW SLAVE STATUS 的 Last_Error 字段。

3. Docker Compose 模拟：主库 docker stop → 从库 1 执行 STOP SLAVE + RESET SLAVE ALL + read_only=OFF → 从库 2 CHANGE MASTER 指向从库 1。验证：插入从库 1，检查从库 2 是否同步。

4. STATEMENT：`mysqlbinlog` 显示 `UPDATE user SET age = age + 1`（语句本身）。ROW：显示每一行被修改前后的值（如 `### @1=1 @2='old' ### @1=1 @2='new'`）。
