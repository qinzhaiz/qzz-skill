# 练习

## 基础练习

1. 建一张 `course` 表，要求：id 主键自增，name 不允许为空且唯一，credit 默认为 3。

2. 建一张 `score` 表，用外键关联到 student 和 course 表。插一条 score 里引用不存在的 student，看看 MySQL 报什么错。

## 进阶练习

1. PRIMARY KEY 和 UNIQUE NOT NULL 有什么区别？试建一张表，用 UNIQUE NOT NULL 代替 PRIMARY KEY，再用 `SHOW CREATE TABLE` 看看 MySQL 内部怎么处理。

2. 外键在什么情况下会成为性能瓶颈？想一个场景。

## 答案

1. 无标准答案。

2. 高并发写入时——每次 INSERT 都要去父表查外键是否存在，涉及锁和索引查找。用户量大的互联网公司通常在应用层做校验。但这不意味着你不用学外键——团队项目、企业系统、金融系统里，数据正确性比性能优先，外键是标配。
