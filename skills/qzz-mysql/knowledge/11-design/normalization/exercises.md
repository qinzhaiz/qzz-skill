# 练习

## 基础练习

1. 判断下面这行数据违反了哪个范式：
```sql
订单表：order_id, product_id, product_name, quantity, customer_name, customer_phone
主键：(order_id, product_id)
```sql

2. 举一个 2NF 但不满足 3NF 的例子。

## 进阶练习

1. 设计一个"员工管理系统"的表结构——包括员工、部门、项目。每个员工属于一个部门，可以参与多个项目（每个项目有多个员工），记录每个员工在每个项目中的角色和投入百分比。确保符合 3NF。

2. 举例说明什么场景下反范式化是合理的，以及如何权衡。

## 答案

1. `product_name` 违反 2NF（只依赖 product_id），`customer_name` 和 `customer_phone` 违反 2NF（只依赖 order_id）。需要拆分：订单表、产品表、客户表、订单明细表。

2. 员工表：（员工 ID，姓名，部门 ID，部门名称）。`部门名称` 通过 `部门 ID` 可以确定，而 `部门 ID` 不是主键——违反了 3NF。拆分为员工表（员工 ID，姓名，部门 ID）和部门表（部门 ID，部门名称）。

3. 核心表：`employee(id, name, dept_id FK)`, `department(id, name)`, `project(id, name)`, `project_member(employee_id, project_id, role, percentage)`。中间表 `project_member` 额外存了角色和投入百分比——这些属于"员工和项目的关系"，不是冗余。

4. 反范式化合理场景：电商订单表冗余存 `username`——查询订单列表是高频操作（每秒数百次），用户改名是低频操作（每天几次）。用少量的一致性风险换大幅性能提升。但需要做好补偿机制（用户改名时更新订单表的 username）。
