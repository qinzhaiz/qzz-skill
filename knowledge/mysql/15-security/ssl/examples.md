# 代码示例

## 示例 1：查看和启用 SSL

```sql
-- 查看 SSL 相关配置
SHOW VARIABLES LIKE '%ssl%';
-- have_ssl: YES（支持 SSL）
-- ssl_ca, ssl_cert, ssl_key: 证书文件路径

-- 查看当前 SSL 连接状态
SHOW STATUS LIKE 'Ssl_cipher';
-- Ssl_cipher: TLS_AES_256_GCM_SHA384（当前加密算法）

-- 强制所有 TCP 连接使用 SSL
SET GLOBAL require_secure_transport = ON;
-- 启用后，非 SSL 的 TCP 连接会被拒绝
-- 注意：localhost 的 socket 连接不受影响
```

## 示例 2：创建 SSL 用户

```sql
-- 创建只允许 SSL 连接的账户
CREATE USER 'secure_app'@'%'
  IDENTIFIED BY 'StrongPass!234'
  REQUIRE SSL;

-- 创建需要 X509 证书的账户（双向认证）
CREATE USER 'high_secure'@'%'
  IDENTIFIED BY 'VeryStrong!567'
  REQUIRE X509;

-- 创建只允许特定加密算法的账户
CREATE USER 'modern_client'@'%'
  IDENTIFIED BY 'Modern@890'
  REQUIRE CIPHER 'TLS_AES_256_GCM_SHA384';

-- 查看哪些用户要求 SSL
SELECT user, host, ssl_type
FROM mysql.user
WHERE ssl_type != '';
```

## 示例 3：生成 SSL 证书

```bash
# MySQL 8.0 自带 mysql_ssl_rsa_setup 工具
# 生成自签名证书（开发环境用）
mysql_ssl_rsa_setup --datadir=/var/lib/mysql

# 生产环境：用 OpenSSL 生成 CA 签发的证书
# 1. 生成 CA 私钥和证书
openssl genrsa 2048 > ca-key.pem
openssl req -new -x509 -nodes -days 3650 -key ca-key.pem -out ca.pem

# 2. 生成服务器私钥和证书请求
openssl req -newkey rsa:2048 -days 3650 -nodes \
  -keyout server-key.pem -out server-req.pem
openssl rsa -in server-key.pem -out server-key.pem

# 3. 用 CA 签发服务器证书
openssl x509 -req -in server-req.pem -days 3650 \
  -CA ca.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem

# 4. 配置 MySQL 使用证书（my.cnf）
# [mysqld]
# ssl_ca=/etc/mysql/certs/ca.pem
# ssl_cert=/etc/mysql/certs/server-cert.pem
# ssl_key=/etc/mysql/certs/server-key.pem

# 5. 重启 MySQL 后验证
mysql -u root -p --ssl-mode=REQUIRED -e "SHOW STATUS LIKE 'Ssl_cipher';"
```

## 示例 4：检查连接是否加密

```sql
-- 查看当前会话的 SSL 信息
SELECT * FROM performance_schema.session_status
WHERE VARIABLE_NAME IN ('Ssl_version', 'Ssl_cipher');

-- 查看所有连接的 SSL 状态
SELECT thd_id, 
       attr_name, 
       attr_value 
FROM performance_schema.session_connect_attrs
WHERE attr_name IN ('_client_name', 'program_name')
   OR attr_name LIKE '%ssl%';

-- 或在命令行查看
-- mysql> \s
-- SSL: Cipher in use is TLS_AES_256_GCM_SHA384

-- 测试：强制 SSL 连接
-- mysql -u app -p  （如果 require_secure_transport=ON，不用 --ssl 会被拒绝）
```
