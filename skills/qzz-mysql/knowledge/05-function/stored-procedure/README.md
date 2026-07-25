# 存储过程

> 存储过程是把一组 SQL 打包存在数据库里，给它起个名字，以后直接调用。

## 为什么需要它

你有一个"创建订单"的操作——需要检查库存、扣库存、插订单、插订单明细。四步操作，如果每次都在应用代码里逐条发 SQL，来回四趟网络往返。

把这四步写成一个存储过程——应用端只发一条 `CALL create_order(...)`，数据库内部完成全部操作。**减少网络往返，逻辑封装在数据库侧。**

## 基本语法

### 创建

```sql
DELIMITER //

CREATE PROCEDURE get_user_count(IN city_name VARCHAR(20), OUT cnt INT)
BEGIN
  SELECT COUNT(*) INTO cnt FROM user WHERE city = city_name;
END //

DELIMITER ;
```sql

- `DELIMITER` 切换结束符——因为过程内部有分号，需要告诉 MySQL "这个分号不是结束"
- `IN` — 输入参数
- `OUT` — 输出参数（过程改它，调用方读）
- `BEGIN ... END` — 过程体，可以放多条 SQL

### 调用

```sql
CALL get_user_count('北京', @result);
SELECT @result;  -- 查看输出
```sql

### 删除

```sql
DROP PROCEDURE IF EXISTS get_user_count;
```sql

## 实际例子

```sql
DELIMITER //

CREATE PROCEDURE create_order(
  IN p_user_id INT,
  IN p_amount DECIMAL(10,2)
)
BEGIN
  DECLARE order_id INT;

  INSERT INTO orders (user_id, amount) VALUES (p_user_id, p_amount);
  SET order_id = LAST_INSERT_ID();

  SELECT order_id AS new_order_id;
END //

DELIMITER ;
```sql

调用：`CALL create_order(1, 100.00);`——一行搞定。

## 优缺点

| 优点 | 缺点 |
|------|------|
| 减少网络往返 | 调试困难——没法打断点 |
| 封装业务逻辑 | 版本管理不方便（不像代码有 git） |
| 权限控制更细 | 数据库成为逻辑中心——扩展性受限 |

## 现代趋势

存储过程在 2000 年代很流行——业务逻辑全放数据库。现在的趋势是"数据库只管存储，业务逻辑放应用层"。原因：

- 应用服务器容易水平扩展，数据库不容易
- 代码有 git、CI/CD、单元测试，存储过程没有
- 跨数据库迁移时存储过程要重写

**知道怎么写就行——实际项目里优先考虑应用层。**

## 注意事项

- **DELIMITER 不是 SQL 的一部分。** 它是 mysql 客户端命令——只在命令行里需要。Workbench 和程序代码里不需要。
- **变量用 `DECLARE` 声明，必须在 BEGIN 之后的最前面。**
- **存储过程内部可以写 IF、LOOP、CASE 等流程控制语句。**

## 和什么有关

- [03-dml/insert/](../../03-dml/insert/) — 存储过程经常包含 INSERT
- [07-transaction/](../../07-transaction/) — 存储过程里的事务控制
