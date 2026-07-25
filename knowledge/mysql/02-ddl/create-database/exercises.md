# 练习

## 基础练习

1. 建一个叫 `bookstore` 的数据库，指定字符集为 `utf8mb4`。用 `SHOW DATABASES` 确认它出现了。

2. 进入 `bookstore`，用 `SELECT DATABASE()` 确认你在正确的库里。

3. 建完再删掉它（`DROP DATABASE`），用 `SHOW DATABASES` 确认它不在了。

## 进阶练习

1. 用 `SHOW CREATE DATABASE mysql;` 看看 MySQL 自带的系统库是怎么建的。它的字符集和排序规则是什么？

2. 不指定 `CHARACTER SET`，建一个库，然后用 `SHOW CREATE DATABASE` 看看 MySQL 给它默认用了什么字符集。

## 答案

1-3 无标准答案，关键是流程跑通。

4-5 取决于你的 MySQL 版本和配置。MySQL 8.0 默认 `utf8mb4` + `utf8mb4_0900_ai_ci`。
