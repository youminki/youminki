import os
import feedparser
from xml.sax.saxutils import escape

SVG_DIR = "svg_cards"
README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.md")
START_TAG = "<!-- BLOG-POST-START -->"
END_TAG = "<!-- BLOG-POST-END -->"

# GitHub Repository 이름 추출 (예: dalcheonroadhead/svg-blog)
repo_name = os.environ.get("GITHUB_REPOSITORY", "dalcheonroadhead/dalcheonroadhead")

# 티스토리 RSS에서 최근 글 5개 파싱
feed = feedparser.parse("https://dalcheonroadhead.tistory.com/rss")
entries = feed.entries[:6]

# SVG → PNG 변환 및 README에 들어갈 <img> 라인 준비
# SVG → PNG 변환 및 README에 들어갈 <img> 라인 준비 (2열 테이블로)
svg_lines = ["<table>"]
for i, entry in enumerate(entries):
    if i % 2 == 0:
        svg_lines.append("  <tr>")

    link = escape(entry.link)
    svg_url = f"https://raw.githubusercontent.com/{repo_name}/main/scripts/{SVG_DIR}/card_{i+1}.svg"
    svg_lines.append(f'''    <td align="center">
        <a href="{link}" target="_blank">
            <img src="{svg_url}" />
        </a>
    </td>''')

    if i % 2 == 1 or i == len(entries) - 1:
        svg_lines.append("  </tr>")
svg_lines.append("</table>")


# README.md 내용 갱신
with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

start = content.find(START_TAG)
end = content.find(END_TAG)

if start != -1 and end != -1:
    new_block = START_TAG + "\n" + "\n".join(svg_lines) + "\n" + END_TAG
    updated = content[:start] + new_block + content[end + len(END_TAG):]

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
