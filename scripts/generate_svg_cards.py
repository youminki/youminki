import feedparser
import os
from datetime import datetime
from xml.sax.saxutils import escape
import base64

RSS_URL = "https://dalcheonroadhead.tistory.com/rss"
MAX_ITEMS = 6
CARD_WIDTH = 600

def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")

base_path = os.path.dirname(__file__)
svg_path = os.path.join(base_path, "svg_cards")
image_path = os.path.join(base_path, "asset", "tistory_background.png")
background_base64 = get_base64_image(image_path)

print("[DEBUG] base_path:", base_path)
print("[DEBUG] image_path:", image_path)
print("[DEBUG] 파일 존재 여부:", os.path.exists(image_path))


SVG_TEMPLATE = """
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
    <image href="data:image/png;base64,{background_base64}" x="0" y="0" width="100%" height="100%" />
    <text x="24" y="40" font-size="14" font-weight="bold" fill="#FFF2CE" text-anchor="{anchor}">dalchoenroadhead.tistory.com</text>
    <text x="24" y="80" font-size="18" font-weight="bold" fill="#FFF2CE" text-anchor="{anchor}">{title}</text>
    {tags_svg}
    <text x="24" y="180" font-size="14" fill="#FFF2CE" text-anchor="{anchor}">{pub_date}</text>
</svg>
"""

def format_tags(tags, x_offset):
    svg_tags = []
    current_x = x_offset
    for tag in tags:
        width = max(len(tag) * 8 + 15, 35)
        svg_tags.append(f'<rect x="{current_x}" y="125" rx="8" ry="8" width="{width}" height="20" fill="#FFF2CE"/>')
        svg_tags.append(f'<text x="{current_x + 6}" y="139" font-weight="bold" font-size="10" fill="#FF6969">{escape(tag)}</text>')
        current_x += width + 10
    return "\n    ".join(svg_tags)

def main():
    os.makedirs(svg_path, exist_ok=True)
    feed = feedparser.parse(RSS_URL) # Parsing 하기 

    for i, entry in enumerate(feed.entries[:MAX_ITEMS]):
        try:
            title = escape(entry.title)
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
            else:
                date = "Unknown"
            tags = [tag.term for tag in entry.get("tags", [])] if "tags" in entry else []

            print(f"[DEBUG] {i+1}. {title} ({date}) - {tags}")

            svg = SVG_TEMPLATE.format(
                title=title,
                pub_date=date,
                tags_svg=format_tags(tags, 24),
                anchor="start",
                background_base64 = background_base64
            )

            filepath = os.path.join(svg_path, f"card_{i+1}.svg")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"[OK] SVG 생성 완료 → {filepath}")

        except Exception as e:
            print(f"[ERROR] {i+1}번 entry 생성 실패: {e}")

if __name__ == "__main__":
    main()
