# 用户与权限管理

> 不要给所有人 root 权限——MySQL 有一套精细的权限系统，用好了能防止 90% 的安全事故。

## 为什么需要它

刚装好 MySQL，只有一个 root 用户，什么都能干。大部分开发环境直接拿这个 root 账户连接——这是最危险的做法。生产环境应该：每个应用有独立账户、每个账户只能访问自己的数据库、只给必要的权限（SELECT/INSERT/UPDATE，不需要 DROP 和 ALTER）。

## 它是什么

MySQL 的权限系统是**用户@主机**粒度的——同一个用户名 `app` 从不同 IP 连接，可以有不同的权限。权限分为多个层级：

| 层级 | 举例 | 权限范围 |
|------|------|---------|
| 全局 | `*.*` | 所有数据库的所有表 |
| 数据库 | `mydb.*` | 指定数据库的所有表 |
| 表 | `mydb.user` | 指定表 |
| 列 | `mydb.user.name` | 指定列 |
| 存储过程 | `PROCEDURE mydb.myproc` | 指定存储过程 |

### 常用权限

| 权限 | 能力 | 风险等级 |
|------|------|---------|
| `ALL PRIVILEGES` | 所有权限 | 🔴 极高 |
| `SELECT` | 读数据 | 🟡 低 |
| `INSERT, UPDATE, DELETE` | 写数据 | 🟡 中 |
| `CREATE, ALTER, DROP` | 修改表结构 | 🔴 高 |
| `FILE` | 读写服务器文件 | 🔴 极高 |
| `SUPER` | 管理操作（KILL, CHANGE MASTER 等） | 🔴 极高 |
| `REPLICATION SLAVE` | 复制 | 🟡 中 |
| `GRANT OPTION` | 能把权限给别人 | 🔴 高 |

## 怎么工作

### 最小权限原则

每个账户只给完成工作必需的权限，不多不少：
- 应用账户：`SELECT, INSERT, UPDATE, DELETE` — 不给 DROP、ALTER
- 只读账户（报表）：`SELECT` — 只读
- 备份账户：`SELECT, RELOAD, LOCK TABLES` — 备份需要
- DBA 个人账户：`ALL PRIVILEGES` — 但不用 root，便于审计

### 权限验证流程

```sql
客户端连接 → 身份验证（用户名+密码）
           → 匹配 host（同用户不同 host 可以有不同权限）
           → 连接建立后权限缓存在内存中
           → 每次操作检查是否有对应权限
```sql

## 怎么用

```sql
-- 创建用户（MySQL 8.0 必须用 CREATE USER）
CREATE USER 'app'@'%' IDENTIFIED BY 'StrongPass123!';
CREATE USER 'readonly'@'10.0.0.%' IDENTIFIED BY 'ReadOnly456!';

-- 授予权限
GRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'app'@'%';
GRANT SELECT ON mydb.* TO 'readonly'@'10.0.0.%';

-- 授予备份权限
GRANT SELECT, RELOAD, LOCK TABLES, PROCESS ON *.* TO 'backup'@'localhost';

-- 查看用户权限
SHOW GRANTS FOR 'app'@'%';

-- 撤销权限
REVOKE DELETE ON mydb.* FROM 'app'@'%';

-- 删除用户
DROP USER 'app'@'%';

-- 刷新权限（修改权限表后一般不需要，GRANT 立即生效）
FLUSH PRIVILEGES;

-- 查看所有用户
SELECT user, host FROM mysql.user;

-- 强制使用安全密码策略
SHOW VARIABLES LIKE 'validate_password%';
SET GLOBAL validate_password.policy = STRONG;  -- 8.0 新语法
```sql

## 注意事项

1. **不要用 `%` 通配所有 host**——如果业务允许，限制 IP 段。`app@'%'` 允许从任何地方连接，增加了安全风险。
2. **MySQL 8.0 不能通过 `GRANT` 隐式创建用户**——必须先用 `CREATE USER` 创建，再用 `GRANT` 授权。早期版本可以省略。
3. **定期审计权限**——检查有没有不再使用的账户、权限过大的账户。`SELECT * FROM mysql.user WHERE user NOT IN ('mysql.session', 'mysql.sys', 'root')`。
4. **应用账户不要用 root**——出了问题排查困难，且 root 可以做任何事（包括 `DROP DATABASE`）。

## 和什么有关

- [SSL/TLS 加密连接](../ssl/) —— 密码和权限的安全传输
- [SQL 注入防护](../sql-injection/) —— 权限管理 + 参数化查询 = 安全的数据库访问层
