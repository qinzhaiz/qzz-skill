# 练习

## 基础练习

1. 创建一个叫 `test_db` 的数据库，进去，建一张叫 `book` 的表（至少包含 id、title、author 三个列），插入 3 本书，用 SELECT 查出来。

2. 在上面那张表上，试验 `SELECT *`、`SELECT title`、`SELECT title, author` 三种写法，看看返回结果有什么不同。

3. 用 `WHERE` 过滤——只查出某一位作者的书。

## 进阶练习

1. 试试在 `CREATE TABLE` 里加一个价格列（`price DECIMAL(10,2)`），插入几本书，跑 `SELECT title, price FROM book WHERE price > 30;`

2. 用 `DESC` 查看 `mysql` 系统库里有什么表。`USE mysql; SHOW TABLES;`——看看 MySQL 自己是怎么组织数据的。看完后 `USE test_db;` 回到你自己的库。

## 答案

练习题没有标准答案——关键是你能在 `mysql>` 里跑通流程，看到正确的输出。
