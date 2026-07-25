# 代码示例

## 示例 1：悲观锁——库存扣减

**场景**：秒杀场景，防止超卖。

```sql
-- 表结构
CREATE TABLE product (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    stock INT NOT NULL
);
INSERT INTO product VALUES (1, '限量杯子', 100);

-- 扣库存的正确姿势（悲观锁）
BEGIN;
-- 用 FOR UPDATE 锁住这一行，别人不能同时改
SELECT stock FROM product WHERE id = 1 FOR UPDATE;
-- 应用层判断：stock > 0？
-- stock 当前 = 100，减 1
UPDATE product SET stock = stock - 1 WHERE id = 1;
COMMIT;
```sql

**为什么必须是 FOR UPDATE？** 如果没有 FOR UPDATE，两个事务可能同时读到 stock=100，都执行 -1，最终 stock=99（少卖了一件）。FOR UPDATE 保证"读 → 判断 → 写"是串行的。

## 示例 2：乐观锁——版本号

**场景**：用户编辑个人资料。

```sql
-- 表结构（version 是乐观锁的关键）
CREATE TABLE user (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    version INT NOT NULL DEFAULT 1
);
INSERT INTO user VALUES (1, '张三', 20, 1);

-- 用户 A 打开编辑页面（读出 version=1）
SELECT id, name, age, version FROM user WHERE id = 1;
-- version = 1

-- 用户 B 也在编辑，先提交了（把 version 改成了 2）
UPDATE user SET name = '张三改名', version = version + 1
WHERE id = 1 AND version = 1;
-- affected_rows = 1（B 成功了，version 变成 2）

-- 用户 A 提交（version 还是 1）
UPDATE user SET age = 25, version = version + 1
WHERE id = 1 AND version = 1;
-- affected_rows = 0！（version 已经是 2 了，WHERE 条件不满足）

-- 应用层判断 affected_rows == 0 → 提示用户"数据已被修改，请刷新重试"
```sql

## 示例 3：乐观锁的应用层重试

**场景**：用应用层代码处理乐观锁更新失败。

```python
# Python 示例——乐观锁重试逻辑
def update_user(user_id, new_age, max_retries=3):
    for retry in range(max_retries):
        # 1. 读当前版本
        cur = db.execute(
            "SELECT id, age, version FROM user WHERE id = %s",
            (user_id,)
        )
        row = cur.fetchone()
        current_version = row['version']

        # 2. 带版本号更新
        db.execute("BEGIN")
        db.execute(
            "UPDATE user SET age = %s, version = version + 1 "
            "WHERE id = %s AND version = %s",
            (new_age, user_id, current_version)
        )
        db.execute("COMMIT")

        # 3. 检查 affected_rows
        if cursor.rowcount == 1:
            return True  # 成功

        # 4. 冲突了，重试
        sleep(0.05 * (retry + 1))

    return False  # 重试耗尽
```
