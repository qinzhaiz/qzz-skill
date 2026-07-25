# SSL/TLS 加密连接

> MySQL 客户端和服务器之间的数据传输默认是明文——任何抓包工具都能看到你的 SQL 语句和数据。SSL/TLS 加密连接就是给这个通道装一把锁。

## 为什么需要它

想象一下：应用服务器在 A 机房，MySQL 在 B 机房，中间经过公网。如果不加密，网络上的任何人都可以抓包看到你的查询语句和返回数据——包括用户名、密码、用户个人信息。即使在内网，安全规范也通常要求数据库连接加密。

## 它是什么

MySQL 支持 TLS（Transport Layer Security，SSL 的后继者）加密客户端和服务器之间的连接。启用 TLS 后：

- 客户端和服务器之间传输的数据被加密（防止窃听）
- 可以验证服务器身份（防止中间人攻击）
- 可以要求客户端提供证书（双向认证）

MySQL 8.0 默认自动创建自签名证书，开箱即用——但生产环境应该用自己的 CA 签发证书。

## 怎么工作

```bash
客户端                      MySQL 服务器
   |                            |
   |——→ 请求 SSL 连接 ——————→  |
   |←—— 发送服务器证书 ——————|
   | (验证证书)                 |
   |←——→ 密钥协商 ←——→        |
   |←——→ 加密数据传输 ←——→    |
```sql

1. 客户端发起连接请求
2. 服务器发送自己的 SSL 证书
3. 客户端验证证书（可选：是否验证 CA 签名）
4. 双方协商加密密钥
5. 后续所有数据加密传输

## 怎么用

```sql
-- 查看 SSL 状态
SHOW VARIABLES LIKE '%ssl%';
SHOW STATUS LIKE '%ssl%';

-- 强制所有连接使用加密（生产环境推荐）
SET GLOBAL require_secure_transport = ON;

-- 创建要求 SSL 连接的用户
CREATE USER 'secure_user'@'%' IDENTIFIED BY 'password' REQUIRE SSL;

-- 创建要求 X509 证书认证的用户（双向认证）
CREATE USER 'cert_user'@'%' IDENTIFIED BY 'password' REQUIRE X509;

-- 查看当前连接是否加密
SELECT ssl_version, ssl_cipher FROM performance_schema.status_by_thread
WHERE thread_id = PS_CURRENT_THREAD_ID();

-- 或更简单：
\s  -- mysql 客户端命令行
-- SSL: Cipher in use is TLS_AES_256_GCM_SHA384
```sql

**客户端连接时指定 SSL：**

```bash
# 基础 SSL（加密但不验证证书）
mysql --ssl-mode=REQUIRED -h host -u user -p

# 验证服务器证书（防止中间人）
mysql --ssl-mode=VERIFY_CA \
      --ssl-ca=/path/to/ca.pem \
      -h host -u user -p

# 双向认证（客户端也要提供证书）
mysql --ssl-mode=VERIFY_IDENTITY \
      --ssl-ca=/path/to/ca.pem \
      --ssl-cert=/path/to/client-cert.pem \
      --ssl-key=/path/to/client-key.pem \
      -h host -u user -p
```sql

**JDBC 连接串：**
```sql
jdbc:mysql://host:3306/mydb?useSSL=true&requireSSL=true&verifyServerCertificate=true&trustCertificateKeyStoreUrl=file:/path/to/truststore.jks
```bash

## 注意事项

1. **MySQL 8.0 默认生成自签名证书**——开发环境可以用，生产环境必须用自己的 CA 签发的证书（客户端需要验证 CA）。
2. **SSL 有性能开销**——加密/解密消耗 CPU。但在现代硬件上，这个开销通常 < 5%，相比明文传输的安全风险，完全可以接受。
3. **证书过期需要更新**——如果不更新，客户端连接会失败。做好证书生命周期管理（告警提前 30 天）。
4. **内网也要加密**——安全规范通常要求数据库传输加密，不管是公网还是内网。云厂商的数据库通常默认开启 SSL。

## 和什么有关

- [用户与权限管理](../user-privileges/) —— SSL + 权限控制 = 完整的安全体系
- [SQL 注入防护](../sql-injection/) —— SQL 注入是应用层攻击，SSL 防护的是传输层
