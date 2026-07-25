# 代码示例

## 示例 1：完整的一次连接和断开

```bash
# 终端输入，不是 mysql> 下
$ mysql -u root -p
Enter password: ********

# 连上了，提示符变成 mysql>
mysql> SELECT VERSION();
+-----------+
| VERSION() |
+-----------+
| 8.0.36    |
+-----------+
1 row in set (0.00 sec)

mysql> quit
Bye

# 回到了终端
$
```sql

整个过程：打开终端 → 输入连接命令 → 输入密码 → 出现 `mysql>` → 跑一条 SQL → `quit` 退出。

## 示例 2：连接远程服务器

```bash
# 连接 IP 为 192.168.1.100 上的 MySQL
mysql -u root -p -h 192.168.1.100 -P 3306
```sql

| 参数 | 含义 |
|------|------|
| `-u root` | 用户名 |
| `-p` | 密码（回车后输入） |
| `-h` | 服务器地址（不写默认 localhost） |
| `-P` | 端口（大写 P，不写默认 3306） |

学习阶段 `-h` 和 `-P` 用不到——你的 MySQL 就在本机。等你上线了自己的项目，连远程数据库时才需要。

## 示例 3：查看 MySQL 服务状态

```bash
# Windows (PowerShell)
Get-Service MySQL80

# Mac
brew services list | grep mysql

# Linux
sudo systemctl status mysql
```bash

这些命令告诉你 MySQL 服务有没有在后台运行。`Active: active (running)` = 正常。有问题先检查服务状态，别急着重装。
