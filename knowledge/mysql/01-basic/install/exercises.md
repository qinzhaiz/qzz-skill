# 练习

## 基础练习

1. 在你的电脑上装好 MySQL，连上去，跑 `SELECT VERSION();`

2. 试试 `SHOW DATABASES;`——你看到了几个数据库？哪些是 MySQL 自带的？

3. 用 `quit` 退出，再用 `mysql -u root -p` 重新连一次。重复 3 遍，直到不用查笔记就能连上。

## 进阶练习

1. 试试 `mysql --help`，浏览一下有哪些命令行参数。你能找到指定字符集的参数吗？

2. 如果你有一台云服务器或树莓派，试着在上面装 MySQL，从你的电脑远程连过去。

## 答案

1. 没有标准答案，取决于你的 MySQL 版本。看到 8.x 就行。

2. 通常会看到 `information_schema`、`mysql`、`performance_schema`、`sys`——这四个是 MySQL 自带的系统数据库，**不要删也不要改**。

3. 反复练习，形成肌肉记忆。
