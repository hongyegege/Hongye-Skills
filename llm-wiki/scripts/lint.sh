#!/usr/bin/env bash
# LLM Wiki Lint — 知识库健康巡检脚本
# 用法: bash lint.sh <知识库根目录>
# 产出: 终端输出检查报告，可追加到 log.md

set -euo pipefail

WIKI_ROOT="${1:-.}"
WIKI_ROOT="$(cd "$WIKI_ROOT" && pwd)"

# 颜色
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "======================================"
echo "  LLM Wiki Lint Report"
echo "  Directory: $WIKI_ROOT"
echo "  Date: $(date +%Y-%m-%d)"
echo "======================================"
echo ""

# 系统文件
SYSTEM_FILES="SCHEMA.md INDEX.md log.md INGEST-SOP.md"
ISSUES=0

# ---- Check 1: Source 未编译 ----
echo "## Check 1: Source 未编译"
uncompiled=0
for src in $(find "$WIKI_ROOT" -name "*-source.md" -not -path "*/.git/*" 2>/dev/null); do
  wiki="${src%-source.md}.md"
  if [ ! -f "$wiki" ]; then
    echo -e "  ${RED}MISSING${NC}: $(basename "$wiki") (from $(basename "$src"))"
    uncompiled=$((uncompiled + 1))
  fi
done
if [ "$uncompiled" -eq 0 ]; then
  echo -e "  ${GREEN}PASS${NC}: All sources have compiled wiki pages"
else
  echo -e "  ${RED}FAIL${NC}: $uncompiled uncompiled source(s)"
  ISSUES=$((ISSUES + uncompiled))
fi
echo ""

# ---- Check 2: 失效交叉引用 ----
echo "## Check 2: 失效交叉引用"
broken_links=0
for md in $(find "$WIKI_ROOT" -name "*.md" -not -name "*-source.md" -not -path "*/.git/*" -not -name "SCHEMA.md" -not -name "INDEX.md" -not -name "log.md" -not -name "INGEST-SOP.md" 2>/dev/null); do
  dir=$(dirname "$md")
  # 提取 markdown 链接中的 .md 路径
  grep -oP '\]\([^)]*\.md\)' "$md" 2>/dev/null | grep -oP '\(([^)]*\.md)\)' | tr -d '()' | while read -r link; do
    target="$dir/$link"
    if [ ! -f "$target" ]; then
      echo -e "  ${RED}BROKEN${NC}: $(basename "$md") -> $link"
      broken_links=$((broken_links + 1))
    fi
  done
done
if [ "$broken_links" -eq 0 ]; then
  echo -e "  ${GREEN}PASS${NC}: No broken cross-references found"
else
  echo -e "  ${RED}FAIL${NC}: $broken_links broken link(s)"
  ISSUES=$((ISSUES + broken_links))
fi
echo ""

# ---- Check 3: 孤立页面 ----
echo "## Check 3: 孤立页面"
orphans=0
for md in $(find "$WIKI_ROOT" -name "*.md" -not -name "*-source.md" -not -path "*/.git/*" -not -name "SCHEMA.md" -not -name "INDEX.md" -not -name "log.md" -not -name "INGEST-SOP.md" 2>/dev/null); do
  bn=$(basename "$md")
  refs=$(grep -rl "$bn" "$WIKI_ROOT" --include="*.md" 2>/dev/null | grep -v "$md" | grep -v "INDEX.md" | wc -l)
  if [ "$refs" -eq 0 ]; then
    echo -e "  ${YELLOW}ORPHAN${NC}: $bn (not referenced by any page)"
    orphans=$((orphans + 1))
  fi
done
if [ "$orphans" -eq 0 ]; then
  echo -e "  ${GREEN}PASS${NC}: All pages are referenced"
else
  echo -e "  ${YELLOW}WARN${NC}: $orphans orphan page(s)"
fi
echo ""

# ---- Check 4: frontmatter 不完整 ----
echo "## Check 4: frontmatter 完整性"
incomplete_fm=0
for md in $(find "$WIKI_ROOT" -name "*.md" -not -name "*-source.md" -not -path "*/.git/*" -not -name "SCHEMA.md" -not -name "INDEX.md" -not -name "log.md" -not -name "INGEST-SOP.md" 2>/dev/null); do
  first_line=$(head -1 "$md")
  if [ "$first_line" != "---" ]; then
    echo -e "  ${YELLOW}MISSING${NC}: $(basename "$md") has no frontmatter"
    incomplete_fm=$((incomplete_fm + 1))
    continue
  fi
  for field in title type category created updated sources; do
    if ! grep -q "^${field}:" "$md" 2>/dev/null; then
      echo -e "  ${YELLOW}MISSING FIELD${NC}: $(basename "$md") lacks '$field'"
      incomplete_fm=$((incomplete_fm + 1))
    fi
  done
done
if [ "$incomplete_fm" -eq 0 ]; then
  echo -e "  ${GREEN}PASS${NC}: All pages have complete frontmatter"
else
  echo -e "  ${YELLOW}WARN${NC}: $incomplete_fm frontmatter issue(s)"
fi
echo ""

# ---- Check 6: 过时声明 ----
echo "## Check 6: 过时声明"
stale=0
for md in $(find "$WIKI_ROOT" -name "*.md" -not -path "*/.git/*" 2>/dev/null); do
  matches=$(grep -nE "TODO|FIXME|HACK|XXX|待验证|待定|计划中" "$md" 2>/dev/null | head -5)
  if [ -n "$matches" ]; then
    echo -e "  ${YELLOW}STALE${NC}: $(basename "$md")"
    echo "$matches" | head -3 | sed 's/^/    /'
    stale=$((stale + 1))
  fi
done
if [ "$stale" -eq 0 ]; then
  echo -e "  ${GREEN}PASS${NC}: No stale markers found"
else
  echo -e "  ${YELLOW}WARN${NC}: $stale file(s) with stale markers"
fi
echo ""

# ---- Check 7: 命名规范 ----
echo "## Check 7: 命名规范"
bad_names=0
for md in $(find "$WIKI_ROOT" -name "*.md" -not -path "*/.git/*" 2>/dev/null); do
  bn=$(basename "$md")
  if echo "$bn" | grep -qP '[\s]'; then
    echo -e "  ${YELLOW}BAD NAME${NC}: $bn (contains spaces)"
    bad_names=$((bad_names + 1))
  fi
done
if [ "$bad_names" -eq 0 ]; then
  echo -e "  ${GREEN}PASS${NC}: All filenames follow kebab-case"
else
  echo -e "  ${YELLOW}WARN${NC}: $bad_names file(s) with naming issues"
fi
echo ""

# ---- Check 8: INDEX.md 同步 ----
echo "## Check 8: INDEX.md 同步"
if [ -f "$WIKI_ROOT/INDEX.md" ]; then
  actual_wikis=$(find "$WIKI_ROOT" -name "*.md" -not -name "*-source.md" -not -path "*/.git/*" -not -name "SCHEMA.md" -not -name "INDEX.md" -not -name "log.md" -not -name "INGEST-SOP.md" -printf "%f\n" 2>/dev/null | sort)
  indexed_count=$(grep -oP '\[[^\]]+\]\([^)]*\.md\)' "$WIKI_ROOT/INDEX.md" 2>/dev/null | wc -l)
  actual_count=$(echo "$actual_wikis" | grep -c '.' 2>/dev/null || echo 0)
  if [ "$indexed_count" -ge "$actual_count" ]; then
    echo -e "  ${GREEN}PASS${NC}: INDEX covers $indexed_count pages (actual: $actual_count)"
  else
    echo -e "  ${YELLOW}WARN${NC}: INDEX has $indexed_count entries, but $actual_count wiki pages exist"
  fi
else
  echo -e "  ${RED}MISSING${NC}: INDEX.md not found"
fi
echo ""

# ---- Check 9: Source 文件大小 ----
echo "## Check 9: Source 文件完整性"
small_sources=0
for src in $(find "$WIKI_ROOT" -name "*-source.md" -not -path "*/.git/*" 2>/dev/null); do
  size=$(wc -c < "$src")
  if [ "$size" -lt 2048 ]; then
    echo -e "  ${YELLOW}SMALL${NC}: $(basename "$src") ($size bytes, may be incomplete)"
    small_sources=$((small_sources + 1))
  fi
done
if [ "$small_sources" -eq 0 ]; then
  echo -e "  ${GREEN}PASS${NC}: All source files meet size threshold"
else
  echo -e "  ${YELLOW}WARN${NC}: $small_sources source(s) below 2KB threshold"
fi
echo ""

# ---- Summary ----
echo "======================================"
echo "  Summary"
echo "======================================"
total_sources=$(find "$WIKI_ROOT" -name "*-source.md" -not -path "*/.git/*" 2>/dev/null | wc -l)
total_wikis=$(find "$WIKI_ROOT" -name "*.md" -not -name "*-source.md" -not -path "*/.git/*" -not -name "SCHEMA.md" -not -name "INDEX.md" -not -name "log.md" -not -name "INGEST-SOP.md" 2>/dev/null | wc -l)
echo "  Wiki pages: $total_wikis"
echo "  Source files: $total_sources"
echo "  Issues found: $ISSUES (red/critical only)"
echo ""

if [ "$ISSUES" -eq 0 ]; then
  echo -e "  ${GREEN}Overall: HEALTHY${NC}"
else
  echo -e "  ${RED}Overall: NEEDS ATTENTION${NC}"
fi
