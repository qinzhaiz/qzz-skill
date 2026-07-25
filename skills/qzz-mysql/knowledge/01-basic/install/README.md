# 安装 MySQL

> 几分钟把 MySQL 装上，连上，跑通第一条命令。

## 为什么需要它

前面讲了一堆概念。现在到了真正动手的时候——装好 MySQL 才能开始写 SQL。

好消息是：MySQL 的安装非常简单。不管你是 Windows、Mac 还是 Linux，官方都提供了安装包。装完就一个核心动作——**用命令行连上去**。

## 怎么装

### Windows

1. 访问 https://dev.mysql.com/downloads/installer/
2. 下载 `mysql-installer-community-8.0.x.msi`
3. 双击运行，选 "Developer Default"
4. 一路 Next，设置 root 密码（**记住它**）
5. 安装完成后，MySQL 会自动在后台运行

### Mac

```bash
# 推荐用 Homebrew，一行搞定
brew install mysql@8.0
brew services start mysql@8.0
```sql

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install mysql-server-8.0
sudo systemctl start mysql
```sql

## 怎么连接

装好后，打开终端/命令行：

```bash
mysql -u root -p
```sql

输入安装时设置的密码。看到这个提示符就成功了：

```bash
mysql>
```bash

这个 `mysql>` 是 MySQL 的命令行客户端。它看起来很简陋——没有图形界面、没有下拉菜单——但它永远可用，是 MySQL 最可靠的接口。即使你以后用图形化工具（Workbench、Navicat），也应该熟悉命令行。

## 验证安装

连上后跑三条命令确认一切正常：

```sql
SELECT VERSION();       -- 查看版本，应该返回 8.x
SHOW DATABASES;         -- 查看所有数据库
SELECT 'Hello MySQL!';  -- 随便试试
```sql

三条都正常返回结果，说明安装成功。

## 连接失败怎么办

如果看到 `Can't connect to MySQL server`：

- **Windows**：MySQL 服务可能没启动。Win+R → `services.msc` → 找到 `MySQL80` → 右键启动
- **Mac**：`brew services start mysql@8.0`
- **Linux**：`sudo systemctl start mysql`

如果看到 `Access denied for user 'root'`：密码输错了。重新安装时记好密码，或者搜索"MySQL 重置 root 密码"。

## 注意事项

- **root 密码别忘。** 这是你数据库的最高权限账号。忘了重设很麻烦。
- **不要用 root 做开发。** 后面学到 [15-security/user-privileges/](../../15-security/user-privileges/) 时会创建专门的用户。root 只用来管理。
- **3306 端口。** MySQL 默认监听 3306。如果装不上检查一下有没有被别的程序占用。
- **命令行必须分号结尾。** `mysql>` 下每条 SQL 必须用 `;` 或 `\g` 结束。光按回车不执行。

## 和什么有关

- [第一次查询](../first-query/) — 连上之后，跑第一条真正的查询
- [15-security/user-privileges/](../../15-security/user-privileges/) — 创建普通用户，不再用 root
