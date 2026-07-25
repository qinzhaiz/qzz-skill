# 常见错误

## 错误 1：忘记 root 密码

**症状**：`ERROR 1045 (28000): Access denied for user 'root'@'localhost'`

**原因**：密码记错了，或者安装时跳过了密码设置。

**怎么修**：MySQL 8.0+ 在 Windows 上安装时会让你设密码——记好。已经忘了的话，搜索"MySQL 8 reset root password"跟着官方文档重置。**不要用网上那些直接跳过密码验证的黑客脚本。**

## 错误 2：分号忘写

**症状**：敲了 `SELECT 1` 按回车，没反应，光标停在 `->` 上。

**原因**：MySQL 命令行要求每条 SQL 以 `;` 结尾。没写分号它就以为你还没说完。

**怎么修**：在 `->` 后面输入 `;` 然后回车。或者 `\c` 取消当前语句。

## 错误 3：装了 MySQL 但服务没启动

**症状**：`ERROR 2003 (HY000): Can't connect to MySQL server on 'localhost'`

**原因**：MySQL 安装后服务没有自动启动（通常是手动关闭过）。

**怎么修**：Windows 去服务管理器启动 MySQL80；Mac 用 `brew services start mysql@8.4`；Linux 用 `sudo systemctl start mysql`。如果反复启动失败，去 MySQL 错误日志里看原因（Windows 在 `C:\ProgramData\MySQL\MySQL Server 8.4\Data\*.err`）。

## 错误 4：在 mysql> 里输入系统命令

**症状**：在 `mysql>` 提示符下敲 `ls`、`dir`、`cd` 然后报错。

**原因**：`mysql>` 只接受 SQL 语句，不接受操作系统命令。

**怎么修**：系统命令在终端里执行，SQL 在 `mysql>` 里执行——这是两个不同的环境。需要切到系统命令时先 `quit` 退出。
