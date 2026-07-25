# 练习

## 基础练习

1. 查出 user 表里所有的 name 和 city。

2. 查出不重复的城市列表。

3. 给 name 列起个别名叫"姓名"，年龄列起个别名叫"年龄"，查出来看看。

## 进阶练习

1. `SELECT DISTINCT city, age FROM user;` 和 `SELECT DISTINCT city FROM user;` 有什么区别？跑一下看看。

2. 用 LIMIT + OFFSET 实现第 2 页数据（每页 3 条）。

## 答案

1. `DISTINCT city, age` 对 (city, age) 组合去重——同一个城市、同一岁数的行只留一条。和单独 DISTINCT city 完全不是一回事。
