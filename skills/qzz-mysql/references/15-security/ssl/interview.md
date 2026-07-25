# 面试题

## Q1：MySQL 怎么配置 SSL？客户端怎么连接？

**考点**：运维安全基本功。

**回答**：服务端配置三个文件——CA 证书、服务器证书、服务器私钥。在 my.cnf 中指定 `ssl_ca`、`ssl_cert`、`ssl_key` 路径。MySQL 8.0 自带 `mysql_ssl_rsa_setup` 生成自签名证书（开发用）。客户端连接用 `--ssl-mode=REQUIRED`（加密但不验证证书）或 `--ssl-mode=VERIFY_CA`（验证服务器证书），生产环境推荐 VERIFY_CA。全局强制 SSL：`SET GLOBAL require_secure_transport = ON`。

**加分点**：能说出 MySQL 8.0 的 `--ssl-mode` 的几种模式——DISABLED（不用）、PREFERRED（默认，能用就用）、REQUIRED（必须加密）、VERIFY_CA（验证 CA）、VERIFY_IDENTITY（验证主机名）。

## Q2：SSL/TLS 加密的性能开销有多大？值得吗？

**考点**：权衡安全与性能。

**回答**：现代硬件上 TLS 1.3 的额外 CPU 开销通常 < 5%。握手阶段有 RSA/ECDHE 计算开销，但连接池复用连接避免了频繁握手。数据传输阶段用对称加密（AES），有硬件加速。相比明文传输的安全风险（密码泄露、数据窃听、中间人攻击），这个性能代价完全值得。

**加分点**：能说出连接池对 SSL 性能的影响——连接池中的长连接只需要一次 TLS 握手，后续传输只有对称加密的极小开销。能提到云厂商 RDS 默认开启 SSL 作为安全保障。
