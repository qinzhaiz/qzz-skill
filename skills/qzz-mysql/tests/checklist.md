# MySQL 知识库检查清单

每个概念完成后，逐一确认以下项目。

## 内容质量

- [ ] README 控制在 200-500 字
- [ ] 代码示例完整可运行（Copy-Paste 到 MySQL 8.0 直接执行）
- [ ] 中文正文，技术名词保留英文
- [ ] 前置概念已正确链接
- [ ] 无版权内容（包括图片、PDF、付费书籍引用）

## 文件完整性

- [ ] 7 个必须文件齐全（README.md, metadata.yaml, examples.md, exercises.md, mistakes.md, interview.md, references.md）
- [ ] assets/ 目录下的文件有引用

## 元数据

- [ ] metadata.yaml 字段完整
- [ ] prerequisites 列表正确
- [ ] difficulty 级别合理
- [ ] updated 日期为当前日期

## 链接

- [ ] 跨概念引用使用相对路径
- [ ] 外部链接可访问（非付费、非需登录）
- [ ] 无 404 链接

## 校验命令

```bash
# 格式校验
python tools/lint.py

# 元数据校验
python tools/metadata.py

# 生成目录
python tools/toc.py
```
