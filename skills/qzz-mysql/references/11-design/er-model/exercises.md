# 练习

## 基础练习

1. 设计一个"博客系统"的 ER 模型：有用户、文章、评论、标签。画出实体之间的关系，标注一对多/多对多。

2. 解释为什么多对多需要中间表，不能在两方各加一个外键。

## 进阶练习

1. 设计一个"在线教育平台"的 ER 模型：包括学生、教师、课程、章节、作业、提交。画出完整 ER 图并写出建表语句。

## 答案

1. 博客系统关系：用户→文章（一对多），文章→评论（一对多），用户→评论（一对多），文章→标签（多对多，需要中间表 `article_tag`）。

2. 假设两个表 A 和 B：如果 A 表加 `b_id`，那 A 只能关联一个 B，不是"多对多"。如果都加外键数组，违反了原子性（一个字段不能存多个值）。中间表 `(a_id, b_id)` 是最合理的——每一行代表一个关联。

3. 关键表：`student(id,name)`, `teacher(id,name)`, `course(id,title,teacher_id)`, `chapter(id,course_id,title)`, `assignment(id,chapter_id,title)`, `submission(id,assignment_id,student_id,content,score)`。课程→章节一对多，章节→作业一对多，作业→提交一对多，学生→提交一对多。
