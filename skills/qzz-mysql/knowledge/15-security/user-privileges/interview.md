# 面试题

## Q1：MySQL 的权限是怎么管理的？有哪些层级？

**考点**：不只是会用 GRANT，要理解权限体系的粒度。

**回答**：MySQL 权限是"用户@主机"粒度的——同一用户从不同 IP 登录可以有不同的权限。权限层级从大到小：全局（`*.*`）→ 数据库（`mydb.*`）→ 表（`mydb.user`）→ 列（`mydb.user.name`）→ 存储过程。执行操作时 MySQL 从高到低检查：先看全局权限、再看数据库权限、再看表权限。权限信息存在 `mysql` 系统库的 user、db、tables_priv、columns_prov 表中。

**加分点**：能说出 MySQL 8.0 的改进——不能通过 GRANT 隐式创建用户（必须先 CREATE USER），引入了角色（Role）支持（类似 RBAC）。能说出权限表的存储引擎是 InnoDB（8.0 后）。

## Q2：生产中怎么给新建的应用配置数据库权限？

**考点**：安全实践经验。

**回答**：三步走——(1) 建独立账户：`CREATE USER 'appname'@'内网IP段' IDENTIFIED BY '强密码'`，(2) 给最小权限：`GRANT SELECT, INSERT, UPDATE, DELETE ON appname_db.* TO 'appname'@'...'`，(3) 不给危险权限：DROP、ALTER、CREATE、FILE、SUPER、GRANT OPTION。如果应用只需要读，就给 SELECT。如果某些操作确实需要更多权限（如创建临时表），额外添加。

**加分点**：能说出不同的环境策略——开发环境权限可以宽松但不要和生产共用密码，生产环境最小权限 + 强密码策略 + 定期审计。
