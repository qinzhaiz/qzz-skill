# 约束

> 约束是数据的规则——数据必须长成这样，否则拒之门外。

## 为什么需要它

你建了一张 `user` 表，有 `age` 列。理论上可以插一条 `age = -5` 或 `age = 999` 进去——MySQL 不会拦你。

但你的业务逻辑知道这些数字是错的。约束就是把这些"业务规则"告诉 MySQL，让它帮你把关。

## 五种约束

### PRIMARY KEY — 主键

每行数据的唯一标识。一张表只能有一个主键，主键列不能为 NULL。

```sql
id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY
```sql

为什么需要：没有主键你就无法精准地说出"我要改第 3 行"——如果 name 相同你能分清吗？

### FOREIGN KEY — 外键

一个表的列引用另一个表的主键，建立表之间的关系。

```sql
CREATE TABLE orders (
    id      INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNSIGNED NOT NULL,
    amount  DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```sql

含义：`orders.user_id` 必须在 `user` 表里真实存在。这样你不可能插入一条"属于一个不存在用户"的订单。

### NOT NULL — 不能为空

该列不允许存 NULL。

```sql
name VARCHAR(32) NOT NULL
```sql

### UNIQUE — 不能重复

该列的值在整张表中唯一。

```sql
email VARCHAR(100) UNIQUE
```sql

和主键的区别：UNIQUE 可以有多个，允许 NULL（但每列只能有一行为 NULL）。

### DEFAULT — 默认值

插入时不指定该列的值时，自动填入默认值。

```sql
status TINYINT NOT NULL DEFAULT 1,
created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
```sql

## 怎么用

建表时最常用的一组约束：

```sql
CREATE TABLE student (
    id      INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name    VARCHAR(32)  NOT NULL,
    email   VARCHAR(100) NOT NULL UNIQUE,
    age     TINYINT UNSIGNED NOT NULL DEFAULT 18,
    PRIMARY KEY (id)
);
```sql

约束之间的关系：

| 约束 | 允许多个？ | 允许 NULL？ | 核心作用 |
|------|-----------|------------|---------|
| PRIMARY KEY | ❌ 只能一个 | ❌ | 行的唯一标识 |
| FOREIGN KEY | ✅ | ✅ | 表之间的关联 |
| NOT NULL | ✅ | 设为 NOT NULL 就不能 | 强制必填 |
| UNIQUE | ✅ | ✅ | 值不能重复 |
| DEFAULT | ✅ | — | 不填时的默认值 |

## 注意事项

- **外键会影响写入性能。** 每次插入/更新都要去父表检查——在高并发写入场景下，很多公司选择在应用层做校验，不在数据库层设外键。
- **主键选好了就别改。** 改主键 = 重排整张表的数据，线上操作可能锁表几小时。
- **NOT NULL + DEFAULT 是好组合。** 既能防止意外空值，又不用每次 INSERT 都写那列。

## 和什么有关

- [创建表](../create-table/) — 建表时怎么配合约束
- [04-query/join/](../../04-query/join/) — 外键和 JOIN 的关系
- [11-design/normalization/](../../11-design/normalization/) — 范式设计会用到约束
