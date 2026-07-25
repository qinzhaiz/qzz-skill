# 代码示例

## 示例 1：创建应用账户的最佳实践

```sql
-- 1. 创建应用专用账户（限制 IP）
CREATE USER 'myapp'@'10.0.0.%' IDENTIFIED BY 'Str0ng!P@ssw0rd';

-- 2. 只给必需的 CRUD 权限
GRANT SELECT, INSERT, UPDATE, DELETE ON myapp_db.* TO 'myapp'@'10.0.0.%';

-- 3. 不给以下危险权限：
-- ❌ ALTER, DROP（改表结构）
-- ❌ CREATE（创建新表）
-- ❌ FILE（读写服务器文件）
-- ❌ SUPER（管理操作）

-- 4. 验证权限
SHOW GRANTS FOR 'myapp'@'10.0.0.%';
-- Grants for myapp@10.0.0.%
-- GRANT USAGE ON *.* TO ...
-- GRANT SELECT, INSERT, UPDATE, DELETE ON myapp_db.* TO ...
```sql

## 示例 2：只读账户和报表账户

```sql
-- 只读账户（给 BI/报表工具用）
CREATE USER 'report'@'%' IDENTIFIED BY 'Report@Read0nly';
GRANT SELECT ON myapp_db.* TO 'report'@'%';

-- 如果想限制只能查某些表的某些列：
GRANT SELECT (id, name, created_at) ON myapp_db.user TO 'report'@'%';
-- 只能查 user 表的这三列，看不到 email、phone 等敏感字段

-- 备份专用账户
CREATE USER 'backup'@'localhost' IDENTIFIED BY 'Backup#Secret';
GRANT SELECT, RELOAD, LOCK TABLES, PROCESS, REPLICATION CLIENT ON *.*
  TO 'backup'@'localhost';
```sql

## 示例 3：密码安全策略

```sql
-- 查看密码策略
SHOW VARIABLES LIKE 'validate_password%';

-- MySQL 8.0 设置强密码策略
SET GLOBAL validate_password.policy = STRONG;
SET GLOBAL validate_password.length = 12;
SET GLOBAL validate_password.mixed_case_count = 1;
SET GLOBAL validate_password.number_count = 1;
SET GLOBAL validate_password.special_char_count = 1;

-- 测试：尝试创建弱密码会报错
CREATE USER 'weak'@'%' IDENTIFIED BY '123';
-- ERROR 1819: Your password does not satisfy the current policy requirements

-- 正确的强密码
CREATE USER 'strong'@'%' IDENTIFIED BY 'MyStr0ng!P@ss';
-- Query OK

-- 查看所有用户及其权限（审计用）
SELECT user, host, 
       plugin, 
       authentication_string, 
       account_locked 
FROM mysql.user 
WHERE user NOT IN ('mysql.infoschema', 'mysql.session', 'mysql.sys');
```sql

## 示例 4：定期清理和审计

```sql
-- 查找没有密码的用户
SELECT user, host FROM mysql.user WHERE authentication_string = '';

-- 查找可以从任意 IP 连接的账户（风险较高）
SELECT user, host FROM mysql.user WHERE host = '%';

-- 查找拥有 SUPER 权限的用户（应该很少）
SELECT user, host FROM mysql.user WHERE Super_priv = 'Y';

-- 查看最近创建的账户
SELECT user, host, 
       FROM_UNIXTIME(created) AS created_time 
FROM mysql.user 
ORDER BY created DESC;

-- 锁定不用的账户（而不是删除，保留审计记录）
ALTER USER 'unused_app'@'%' ACCOUNT LOCK;
```
