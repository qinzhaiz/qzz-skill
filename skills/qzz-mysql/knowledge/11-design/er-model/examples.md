# 代码示例

## 示例 1：电商系统 ER 设计

**场景**：设计一个简单电商系统的数据库。

**ER 分析**：
- 实体：用户（User）、商品（Product）、订单（Order）
- 关系：
  - 用户 → 订单：一对多（一个用户多个订单）
  - 订单 → 商品：多对多（一个订单包含多个商品，一个商品出现在多个订单中）

```sql
-- 用户表
CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100)
);

-- 商品表
CREATE TABLE product (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0
);

-- 订单表（"多"方存用户外键）
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 订单明细表（多对多中间表，额外存数量和单价）
CREATE TABLE order_item (
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);
```sql

## 示例 2：一对一关系

**场景**：用户和用户详情（拆表减少字段）。

```sql
-- 主表：存常用字段
CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password_hash CHAR(60) NOT NULL
);

-- 扩展表：存不常用的大字段
CREATE TABLE user_profile (
    user_id INT PRIMARY KEY,  -- 主键同时是外键，保证一对一
    avatar_url VARCHAR(500),
    bio TEXT,
    birthday DATE,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```sql

**解释**：`user_profile` 的主键就是 `user_id`——同一个 ID 不可能出现两次，天然保证了一对一。

## 示例 3：自关联（树形结构）

**场景**：部门有上级部门。

```sql
CREATE TABLE department (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    parent_id INT,  -- 指向自己的外键
    FOREIGN KEY (parent_id) REFERENCES department(id)
);
-- 公司 (parent_id=NULL)
--   ├── 技术部 (parent_id=1)
--   │   ├── 前端组 (parent_id=2)
--   │   └── 后端组 (parent_id=2)
--   └── 市场部 (parent_id=1)
```
