# 代码示例

## 示例 1：追踪一条 SELECT 的执行路径

```bash
# 入口：sql/sql_parse.cc -> dispatch_command()
# 分发到 SELECT 处理

# 解析阶段：sql/sql_lex.cc（词法）-> sql/sql_yacc.yy（语法）

# 优化阶段：sql/sql_optimizer.cc
# 关键函数：JOIN::optimize()

# 执行阶段：sql/sql_executor.cc
# 关键函数：JOIN::exec()

# 存储引擎层：sql/handler.cc -> ha_innobase::rnd_next()
# 关键函数：handler::ha_rnd_next() 调存储引擎接口

# InnoDB 层：storage/innobase/row/row0sel.cc
# 关键函数：row_search_mvcc()  B+Tree 查找 + MVCC 可见性判断
```

## 示例 2：关键代码片段（简化版）

```cpp
// sql/sql_parse.cc 简化版——SQL 入口
void dispatch_command(THD *thd, const COM_DATA *com_data) {
    // 1. 解析 SQL
    Parser_state parser_state;
    parse_sql(thd, &parser_state);
    
    // 2. 根据命令类型分发
    switch (command) {
        case COM_QUERY:
            mysql_execute_command(thd);  // 执行 DML/DDL
            break;
    }
}
```

```cpp
// storage/innobase/buf/buf0buf.cc 简化版——Buffer Pool 读取
buf_block_t* buf_page_get(
    const page_id_t& page_id,  // 要读取的页 ID
    ...
) {
    // 1. 在 Buffer Pool 中查找
    block = buf_LRU_get_free_block();  // LRU 淘汰找空闲块
    
    // 2. 如果不在内存中，从磁盘读取
    if (block->page.state != BUF_BLOCK_FILE_PAGE) {
        fil_io(..., page_id, ...);  // 文件 IO
    }
    
    return block;
}
```

## 示例 3：搜索源码中的概念

```bash
# 搜索"幻读"相关代码
grep -r "phantom" storage/innobase/

# 搜索 Next-Key Lock 实现
grep -r "next.key" storage/innobase/lock/

# 搜索 MVCC ReadView
grep -r "ReadView" storage/innobase/read/

# 搜索 B+Tree 分裂逻辑
grep -r "btr_page_split" storage/innobase/btr/

# 查看某个文件的函数列表
ctags -x --c++-kinds=f storage/innobase/lock/lock0lock.cc
```

## 示例 4：用 cloc 了解代码规模

```bash
$ cloc sql/ storage/innobase/

Language   files   blank   comment   code
C++        2500    300k    250k     1.5M
C/C++ Hdr  2000    200k    180k     1.0M
C           300     20k     15k      100k
---------------------------------------------------
SUM:                            ~2.6M (SQL + InnoDB)
```
