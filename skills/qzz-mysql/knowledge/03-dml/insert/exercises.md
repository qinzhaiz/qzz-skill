# 练习

## 基础练习

1. 往 user 表里插 5 条数据，用列名列表的写法。

2. 一次 INSERT 插入 3 行——比单独执行 3 条 INSERT 有什么区别？

3. 试试不列列名的写法（`INSERT INTO user VALUES(...)`），然后 ALTER TABLE 加一列再跑一次，看看报什么错。

## 进阶练习

1. 建一张 `user_backup` 表（和 user 同结构），用 INSERT SELECT 把 user 里城市是北京的用户复制过去。

## 答案

1-3 无标准答案。

4. `INSERT INTO user_backup SELECT * FROM user WHERE city = '北京';`
