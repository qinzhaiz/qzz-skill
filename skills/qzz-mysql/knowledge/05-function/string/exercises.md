# 练习

## 基础练习

1. 拼接用户的 name 和 city，中间用 " - " 隔开。

2. 取所有用户手机号的后 4 位。

3. 查出名字超过 3 个字符的用户（用 CHAR_LENGTH, 不是 LENGTH）。

## 进阶练习

1. CONCAT 里有一个参数为 NULL 时结果是什么？试试看。

## 答案

1. `SELECT CONCAT(name, ' - ', city) FROM user;`

2. `SELECT RIGHT(mobile, 4) FROM user;`

3. `SELECT * FROM user WHERE CHAR_LENGTH(name) > 3;`

4. 结果为 NULL——CONCAT 中任何一个参数为 NULL 则整体返回 NULL。用 CONCAT_WS 或 IFNULL 兜底。
