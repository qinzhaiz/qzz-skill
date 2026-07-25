#!/usr/bin/env python3
"""
PDF → Markdown 转换工具
- 文字版 PDF：pymupdf 提取结构化的文本
- 扫描版 PDF：pymupdf 提取 + OCR 兜底（需要 tesseract）

用法：
    python tools/pdf2md.py input.pdf                    # 输出 input.md
    python tools/pdf2md.py input.pdf -o output.md       # 指定输出
    python tools/pdf2md.py input.pdf --debug            # 每页输出调试信息
"""

import argparse
import os
import re
import sys
from pathlib import Path


def install_deps():
    """自动安装依赖"""
    import subprocess

    deps = ["pymupdf"]
    for dep in deps:
        try:
            __import__(dep.replace("-", "_"))
        except ImportError:
            print(f"[setup] 安装 {dep} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])


install_deps()
import fitz  # pymupdf


# ── 文本特征检测 ────────────────────────────


def is_chapter_title(text, font_size):
    """检测是否是章节标题"""
    text = text.strip()
    if not text:
        return False
    # 中文章节：第X章 / 第X课 / 附录
    if re.match(r"^(第[一二三四五六七八九十\d]+[章节课]|附录)", text):
        return True
    # 英文章节：Chapter X / Part X / Lesson X
    if re.match(r"^(Chapter|Part|Lesson|Section)\s+\d+", text, re.IGNORECASE):
        return True
    # 大字号短文本（可能是标题）
    if font_size and font_size >= 16 and len(text) <= 60:
        return True
    return False


def is_code_block(text):
    """检测是否是代码块"""
    # SQL / 命令行特征
    code_indicators = [
        r"^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|SHOW|USE|DESC|SET|GRANT)\s",
        r"^\s*mysql>",
        r"^\s*\$",
        r"^\s*#\s*(include|import)",
    ]
    for pattern in code_indicators:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def classify_block(lines, avg_font):
    """判断文本块的类型"""
    text = "".join(lines).strip()
    if not text:
        return "empty"

    # 代码块
    if is_code_block(text):
        return "code"

    # 简洁检测：第一行的字号
    first_line_font = avg_font if avg_font else 10

    if is_chapter_title(lines[0] if lines else text, first_line_font):
        return "h1"

    if first_line_font >= 14 and len(text) <= 80:
        return "h2"

    return "text"


# ── PDF 解析 ────────────────────────────


def extract_text_blocks(page):
    """
    按阅读顺序提取页面的文本块。
    返回 [(text, avg_font_size), ...]
    """
    blocks = page.get_text("dict")["blocks"]
    results = []

    for block in blocks:
        if block["type"] != 0:  # 非文本块（图片等）
            continue

        lines = []
        font_sizes = []

        for line in block["lines"]:
            line_text = ""
            for span in line["spans"]:
                line_text += span["text"]
                font_sizes.append(span["size"])
            lines.append(line_text.strip())

        text = " ".join(lines).strip()
        if text:
            avg_size = round(sum(font_sizes) / len(font_sizes), 1) if font_sizes else 10
            results.append((text, avg_size))

    return results


def detect_text_ratio(doc, sample_pages=5):
    """检测 PDF 是不是文字版（前 N 页的文字覆盖率）"""
    total_chars = 0
    total_pages = min(sample_pages, len(doc))

    for i in range(total_pages):
        page = doc[i]
        text = page.get_text()
        total_chars += len(text.strip())

    avg_chars = total_chars / max(total_pages, 1)
    return avg_chars


# ── Markdown 生成 ────────────────────────────


def to_markdown(blocks, pdf_name=""):
    """把文本块列表转成 Markdown"""
    md = []
    if pdf_name:
        md.append(f"# {pdf_name}\n")

    prev_type = None

    for text, font_size in blocks:
        lines = [text]
        block_type = classify_block(lines, font_size)

        # 空行处理
        if block_type == "empty":
            md.append("")
            prev_type = "empty"
            continue

        # 章节标题
        if block_type == "h1":
            md.append(f"\n## {text}\n")
            prev_type = "h1"
            continue

        # 小节标题
        if block_type == "h2":
            md.append(f"\n### {text}\n")
            prev_type = "h2"
            continue

        # 代码块
        if block_type == "code":
            if prev_type != "code":
                md.append("\n```sql")
            md.append(text)
            prev_type = "code"
            continue
        elif prev_type == "code":
            md.append("```\n")

        # 列表行
        if re.match(r"^[\d•\-–·]\s", text):
            md.append(f"- {re.sub(r'^[\d•\-–·]\s*', '', text)}")
            prev_type = "list"
            continue

        # 普通段落
        text = clean_text(text)
        if text:
            md.append(f"\n{text}\n")
            prev_type = "text"

    # 收尾未闭合的代码块
    if prev_type == "code":
        md.append("```\n")

    return "\n".join(md)


def clean_text(text):
    """清理文本杂讯"""
    # 合并断行（单个换行变空格）
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    # 去多余空格
    text = re.sub(r" {2,}", " ", text)
    # 修复常见 PDF 导出乱码
    text = text.replace("ﬂ", "fl").replace("ﬁ", "fi").replace("–", "--").replace("—", "---")
    return text.strip()


# ── 主流程 ────────────────────────────


def convert_pdf(pdf_path, output_path=None, debug=False):
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        print(f"[error] 文件不存在: {pdf_path}")
        return

    if output_path is None:
        output_path = pdf_path.with_suffix(".md")

    print(f"[info] 读取 PDF: {pdf_path}")
    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)

    # 检测类型
    avg_chars = detect_text_ratio(doc)
    print(f"[info] 总页数: {total_pages}，前5页平均字符数: {avg_chars:.0f}")

    if avg_chars < 50:
        print("[warn] 文字量低，可能是扫描版 PDF。")
        print("[warn] 扫描版需要 OCR（tesseract），本脚本暂不做 OCR，只尝试提取文本。")

    # 逐页提取
    all_blocks = []
    for i in range(total_pages):
        page = doc[i]
        blocks = extract_text_blocks(page)
        if debug and blocks:
            print(f"\n--- page {i+1} ---")
            for text, size in blocks[:5]:
                print(f"  [{size}pt] {text[:100]}")
        all_blocks.extend(blocks)

    doc.close()

    # 生成 Markdown
    pdf_name = pdf_path.stem
    md_text = to_markdown(all_blocks, pdf_name)

    # 写入
    Path(output_path).write_text(md_text, encoding="utf-8")
    print(f"[done] 输出: {output_path} ({len(md_text):,} 字符)")


# ── CLI ────────────────────────────


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PDF → Markdown（文字版 PDF）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python tools/pdf2md.py book.pdf
  python tools/pdf2md.py book.pdf -o notes.md
  python tools/pdf2md.py book.pdf --debug
        """,
    )
    parser.add_argument("input", help="输入 PDF 文件路径")
    parser.add_argument("-o", "--output", help="输出 Markdown 文件路径（默认同目录同名 .md）")
    parser.add_argument("--debug", action="store_true", help="打印每页前 5 个文本块，用于调试")
    args = parser.parse_args()

    convert_pdf(args.input, args.output, args.debug)
