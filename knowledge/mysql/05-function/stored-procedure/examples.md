# 代码示例

## 示例 1：无参数存储过程

```sql
DELIMITER //

CREATE PROCEDURE list_beijing_users()
BEGIN
  SELECT * FROM user WHERE city = '北京';
END //

DELIMITER ;

CALL list_beijing_users();
```

## 示例 2：带输入参数

```sql
DELIMITER //

CREATE PROCEDURE get_users_by_city(IN city_name VARCHAR(20))
BEGIN
  SELECT * FROM user WHERE city = city_name;
END //

DELIMITER ;

CALL get_users_by_city('上海');
```

## 示例 3：带输出参数

```sql
DELIMITER //

CREATE PROCEDURE count_users_by_city(
  IN city_name VARCHAR(20),
  OUT cnt INT
)
BEGIN
  SELECT COUNT(*) INTO cnt FROM user WHERE city = city_name;
END //

DELIMITER ;

CALL count_users_by_city('北京', @result);
SELECT @result;
```
