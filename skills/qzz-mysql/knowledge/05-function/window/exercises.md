# 练习

## 基础练习

1. 给所有员工按薪资排名（用 RANK）。

2. 查每个部门内员工的薪资排名。

## 进阶练习

1. ROW_NUMBER、RANK、DENSE_RANK 在并列值上的行为有什么区别？写一个查询验证。

## 答案

1. `SELECT *, RANK() OVER (ORDER BY salary DESC) FROM employee;`

2. `SELECT *, RANK() OVER (PARTITION BY dept ORDER BY salary DESC) FROM employee;`

3. 两行薪资相同时：ROW_NUMBER 给不同序号（1,2），RANK 跳号（1,1,3），DENSE_RANK 不跳号（1,1,2）。
