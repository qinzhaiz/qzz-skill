# 代码示例

## 示例 1：查看 MySQL 版本

```sql
mysql> SELECT VERSION();
+-----------+
| VERSION() |
+-----------+
| 8.4.0     |
+-----------+
```

这是你连上 MySQL 后第一件该做的事——确认版本。不同版本之间 SQL 语法基本通用，但少数特性（如窗口函数需要 8.0+）可能不一样。

## 示例 2：客户端-服务器在同一台机器 vs 不同机器

**场景 A：学习和开发**

```
[你的电脑]
  ├── 客户端（mysql 命令行）
  └── 服务器（mysqld 进程）
       └── 数据文件（/var/lib/mysql/）
```

客户端和服务器在同一台机器。你敲 SQL，本机处理，本机返回。这是你接下来学习时的模式。

**场景 B：生产环境**

```
[你的电脑 / 应用服务器]  ──网络──→  [数据库服务器]
  Java 程序连接                    mysqld 运行在
  jdbc:mysql://192.168.1.100       IP 192.168.1.100
```

你的程序通过网络连接到一台专门的数据库服务器上。你不需要在那台服务器上操作——客户端在你的机器上，服务器在远程。所有 SQL 走网络传过去，结果走网络传回来。

## 示例 3：MySQL vs SQLite 的使用区别

```sql
-- MySQL：需要先连接服务器
mysql -u root -p
mysql> CREATE DATABASE mydb;
mysql> USE mydb;
mysql> CREATE TABLE users (id INT, name VARCHAR(50));

-- SQLite：直接操作文件，无需服务器
sqlite3 mydata.db
sqlite> CREATE TABLE users (id INT, name VARCHAR(50));
```

SQLite 不需要安装服务器，直接对一个文件操作。这就是"嵌入式"和"客户端-服务器"的区别。SQLite 适合本地存配置、App 内嵌数据库；MySQL 适合多用户、多应用同时访问的场景。
