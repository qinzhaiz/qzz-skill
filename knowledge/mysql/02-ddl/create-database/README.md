# 创建数据库

> 建库是你跟 MySQL 说的第一句"我要占一块地方"。

## 为什么需要它

连上 MySQL 后，你面对的是一个空荡荡的系统。系统里虽然有自带的四个库，但那不是你的——你得有一个**自己的数据库**，用来放属于你的表和数据。

建库就是圈地。你先划一块地盘，然后在这块地盘里建表、插数据、做实验。

## 它是什么

**数据库（Database）** 是表、视图、存储过程等对象的容器。一个 MySQL 实例里可以有多个数据库，每个数据库之间互相独立。

和 Excel 的类比：Excel 文件 = 数据库，Sheet（工作表）= 表，行 = 数据。

## 怎么用

### 基本语法

```sql
CREATE DATABASE 数据库名;
```

最简单的就这一行。但实际操作中推荐加上几个选项：

```sql
CREATE DATABASE IF NOT EXISTS mydb
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
```

逐行拆解：

| 部分 | 作用 |
|------|------|
| `IF NOT EXISTS` | 如果库已存在就不重复创建，**不会报错**。不加这行的话重复建库会报错 |
| `CHARACTER SET utf8mb4` | 指定编码为完整 UTF-8，能存中文和 emoji |
| `COLLATE utf8mb4_0900_ai_ci` | 指定排序和比较规则。`ai` = accent insensitive（不区分重音），`ci` = case insensitive（不区分大小写） |

MySQL 8.0 默认就是 `utf8mb4`，但显式写上有两个好处：不会因为服务器被改过默认值而出意外；别人看你代码时一眼就知道编码是什么。

### 建完要选库

```sql
USE mydb;
```

不选库的话，建表、查数据都不知道去哪。每次连上 MySQL 后第一件事就是 USE。

### 删库

```sql
DROP DATABASE IF EXISTS mydb;
```

**这个操作不可逆！** 库里的表和数据全没了。`IF EXISTS` 避免库不存在时报错。

## 注意事项

- **库名只用小写字母、数字和下划线。** `my_project` 可以，`My-Project` 不要。
- **不要在生产环境用 DROP DATABASE。** 删之前确认三遍——你在哪个库、库里有啥、有没有备份。
- **utf8 和 utf8mb4 不是一回事。** MySQL 里的 `utf8` 是阉割版（最多 3 字节），不能存 emoji。永远用 `utf8mb4`。

## 和什么有关

- [创建表](../create-table/) — 建完库，在里面建第一张表
- [01-basic/first-query](../../01-basic/first-query/) — 第一次建库和查询的完整流程
