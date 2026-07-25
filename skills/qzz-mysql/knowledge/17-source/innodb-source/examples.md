# 代码示例

## 示例 1：追踪 SELECT 在 InnoDB 中的执行

```cpp
// 1. Server 层调用 handler/ha_innodb.cc
// ha_innobase::index_read() → row_search_mvcc()

// 2. storage/innobase/row/row0sel.cc
// row_search_mvcc() —— 核心函数！约 2000 行
dberr_t row_search_mvcc(
    byte* buf,          // 返回数据
    page_cur_mode_t mode,
    row_prebuilt_t* prebuilt,
    ...
) {
    // 1. B+Tree 搜索
    btr_pcur_open_with_no_init();  // 打开 B+Tree 游标
    
    // 2. 逐行遍历 + MVCC 检查
    for (;;) {
        rec = btr_pcur_get_rec(&pcur);  // 获取当前记录
        
        // 3. 检查记录是否对当前事务可见
        if (rec_get_deleted_flag(rec, ...)) continue;
        
        // 4. 检查锁（S 锁或 X 锁）
        lock_clust_rec_cons_read_sees(rec, ...);
        
        // 5. 返回数据
        row_sel_store_mysql_rec(buf, prebuilt, rec, ...);
    }
}
```sql

## 示例 2：B+Tree 页分裂

```cpp
// storage/innobase/btr/btr0btr.cc
dberr_t btr_page_split_and_insert(
    btr_cur_t* cursor,   // 插入位置
    ...
) {
    // 1. 分配新页
    new_block = btr_page_alloc(cursor->index, ...);
    
    // 2. 把原页的后半部分记录搬到新页
    // 分裂点通常是页的中间位置
    
    // 3. 更新父页的指针（父页也可能分裂——递归）
    btr_attach_half_pages(...);
    
    // 4. 插入新记录（放到正确的页中）
    btr_cur_insert_rec(...);
}
```sql

## 示例 3：死锁检测

```cpp
// storage/innobase/lock/lock0lock.cc
void lock_deadlock_check_and_resolve(
    const trx_t*      trx,      // 当前被阻塞的事务
    ...
) {
    // 1. 构建等待图
    // 从 trx 开始，追踪它等待的锁 → 找到持有者 → 再看持有者在等谁
    
    // 2. DFS 检测环（O(N²) 复杂度）
    // 如果发现环 → 选择代价最小的事务回滚
    
    // 3. 选择牺牲品（victim）
    // 通常选 undo log 最少的事务（回滚代价最小）
    trx_t* victim = lock_deadlock_select_victim(...);
    
    // 4. 回滚牺牲品
    lock_deadlock_notify(victim);  // 返回错误给客户端
}
```
