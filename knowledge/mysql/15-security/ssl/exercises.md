# 练习

## 基础练习

1. 在你的 MySQL 上执行 `SHOW VARIABLES LIKE '%ssl%'`，查看 SSL 是否已配置。连接到 MySQL 后在命令行输入 `\s`，查看当前连接是否加密。

2. 创建一个需要 SSL 的用户，用 `--ssl-mode=REQUIRED` 连接成功，再用 `--ssl-mode=DISABLED` 连接——应该被拒绝。

## 进阶练习

1. 用 OpenSSL 自建 CA，签发服务器证书和客户端证书，配置 MySQL 启用 SSL。测试双向认证（客户端提供证书才能连接）。

2. 调研你的应用框架（Spring、Django、Express 等）如何配置数据库连接的 SSL。写出完整的配置说明。

## 答案

1. `have_ssl = YES` 表示支持 SSL。如果 `\s` 显示 `SSL: Not in use` 表示当前连接没加密——用 `--ssl-mode=REQUIRED` 重连即可。

2. 创建 `user_ssl` 用户（REQUIRE SSL）。用 `--ssl-mode=DISABLED` 连接 → 报错 `Access denied for user ... SSL required`。用 `--ssl-mode=REQUIRED` 连接 → 成功。

3. CA 签发 → 服务器配置 ca.pem/server-cert.pem/server-key.pem → 客户端配置 ca.pem（验证服务器）+ client-cert.pem/client-key.pem（客户端认证）。双向认证确保双方都是可信的。

4. Spring Boot: `spring.datasource.url=jdbc:mysql://...?useSSL=true&requireSSL=true`。Django: `DATABASES['default']['OPTIONS'] = {'ssl': {'ca': '/path/to/ca.pem'}}`。
