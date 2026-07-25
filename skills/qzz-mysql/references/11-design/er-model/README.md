# ER 模型

> 在写 CREATE TABLE 之前，先用框框和线把数据之间的关系画出来——这就是 ER 模型。

## 为什么需要它

很多人拿到需求就直接建表，建到一半发现关系搞错了——"一个用户可以有多个地址吗？一个订单可以有多个商品吗？"回头改表结构，已经插入了几百万行数据。ER 模型让你在动手写代码之前，先把"有哪些东西、它们之间怎么关联"想清楚。

## 它是什么

ER 模型（Entity-Relationship Model）是数据库设计的蓝图。只有两个核心概念：

- **实体（Entity）**：一个"东西"——用户、订单、商品。对应数据库中的一张表。
- **关系（Relationship）**：两个实体之间的关联。有三种：

| 关系 | 例子 | 怎么实现 |
|------|------|---------|
| **一对一** | 用户 ↔ 身份证号 | 任一张表加外键 + UNIQUE |
| **一对多** | 用户 → 订单 | "多"的那方加外键 |
| **多对多** | 学生 ↔ 课程 | 建中间表（两个外键） |

## 怎么工作

ER 图用矩形表示实体，菱形表示关系，连线表示关联。

```
[学生] ———<选课>——— [课程]
  |                   |
 多                  多

实现为：
学生表 (id, name)
课程表 (id, title)
选课表 (student_id, course_id, score)  ← 中间表
```

### 设计步骤

1. **找实体**：需求文档里的名词 → 用户、商品、订单、评论
2. **定属性**：每个实体有哪些字段
3. **找关系**：实体之间怎么关联？（一个用户有多个订单 → 一对多）
4. **画 ER 图**：用工具（Draw.io、MySQL Workbench）画出来，和团队确认

## 怎么用

```sql
-- 一对多：用户和订单
CREATE TABLE user (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES user(id)  -- "多"方存外键
);

-- 多对多：学生和课程（需要中间表）
CREATE TABLE student (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE course (
    id INT PRIMARY KEY,
    title VARCHAR(100)
);

CREATE TABLE enrollment (  -- 中间表
    student_id INT,
    course_id INT,
    score INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (course_id) REFERENCES course(id)
);
```

## 注意事项

1. **多对多关系必须有中间表**——不能在两方各存一个外键（会导致数据冗余和不一致）。
2. **ER 图不是越复杂越好**——如果一张 ER 图有 50+ 个实体，拆成多个子模块分别画。
3. **现实世界的关系要"翻译"成数据库关系**——"一个人有两辆车"不一定是多对多（可能一辆车只有一个车主）。

## 和什么有关

- [范式设计](../normalization/) —— ER 模型画出来后，用范式检查是否合理
- [表创建](../../02-ddl/create-table/) —— ER 模型最后变成 CREATE TABLE
- [外键约束](../../02-ddl/constraints/) —— 关系的实现方式
- [常见设计模式](../design-patterns/) —— 具体场景的建表套路
