#!/usr/bin/env python3
"""Build rnh.bio: posts/*.md -> _site/

Usage:
    python build.py           build into _site/
    python build.py --serve   build, then serve at http://localhost:8000
"""
import math
import re
import shutil
import sys
import tomllib
from datetime import datetime, timezone
from email.utils import format_datetime
from functools import partial
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"
SITE = tomllib.loads((ROOT / "site.toml").read_text())
MD = markdown.Markdown(extensions=["fenced_code", "tables", "footnotes", "md_in_html"])


def template(name, **ctx):
    """Fill {{ key }} placeholders. Inserted values are never re-scanned."""
    text = (ROOT / "templates" / name).read_text()
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda m: str(ctx[m.group(1)]), text)


def nav_links():
    links = ['<a href="/">writing</a>']
    if SITE.get("github"):
        links.append(f'<a href="https://github.com/{escape(SITE["github"])}">github</a>')
    if SITE.get("email"):
        links.append(f'<a href="mailto:{escape(SITE["email"])}">email</a>')
    links.append('<a href="/feed.xml">rss</a>')
    return "".join(links)


def page(title, body, description=None):
    return template(
        "base.html",
        title=escape(title),
        description=escape(description or SITE["description"]),
        site=escape(SITE["title"]),
        nav=nav_links(),
        body=body,
    )


def read_post(path):
    """Split optional front matter (key: value lines between --- fences) from the body."""
    raw = path.read_text()
    meta = {}
    if raw.startswith("---\n"):
        head, _, raw = raw[4:].partition("\n---\n")
        for line in head.splitlines():
            key, sep, value = line.partition(":")
            if sep:
                meta[key.strip().lower()] = value.strip().strip("\"'")
    return meta, raw


def parse_date(value, path):
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    sys.exit(f"{path.name}: can't read date {value!r} (use YYYY-MM-DD or YYYY-MM-DD HH:MM)")


def load_posts():
    posts = []
    for path in sorted((ROOT / "posts").glob("*.md")):
        meta, source = read_post(path)
        if meta.get("draft", "").lower() == "true":
            continue
        m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", path.stem)
        if "date" in meta:
            date = parse_date(meta["date"], path)
        elif m:
            date = parse_date(m.group(1), path)
        else:
            sys.exit(f"{path.name}: needs a date in front matter or a YYYY-MM-DD filename prefix")
        slug = m.group(2) if m else path.stem
        MD.reset()
        body = MD.convert(source)
        words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", body)))
        posts.append({
            "slug": slug,
            "title": meta.get("title", slug.replace("-", " ")),
            "description": meta.get("description", ""),
            "date": date,
            "body": body,
            "minutes": max(1, math.ceil(words / 230)),
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "static", OUT / "static")
    if (ROOT / "images").exists():
        shutil.copytree(ROOT / "images", OUT / "images")

    posts = load_posts()

    for i, p in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        links = []
        if newer:
            links.append(f'<a href="/writing/{newer["slug"]}/">newer: {escape(newer["title"])}</a>')
        if older:
            links.append(f'<a href="/writing/{older["slug"]}/">older: {escape(older["title"])}</a>')
        links.append('<a href="/">back to writing</a>')
        html = page(
            p["title"],
            template(
                "post.html",
                title=escape(p["title"]),
                iso=p["date"].date().isoformat(),
                date=p["date"].strftime("%d %b %Y"),
                minutes=p["minutes"],
                content=p["body"],
                links="<br>\n".join(links),
            ),
            description=p["description"] or None,
        )
        out = OUT / "writing" / p["slug"]
        out.mkdir(parents=True)
        (out / "index.html").write_text(html)

    items = "\n".join(
        f'<li><a href="/writing/{p["slug"]}/">{escape(p["title"])}</a> '
        f'<span class="m">({p["date"].strftime("%b %Y")})</span></li>'
        for p in posts
    )
    updated = posts[0]["date"].strftime("%d %b %Y") if posts else datetime.now().strftime("%d %b %Y")
    (OUT / "index.html").write_text(
        page(SITE["title"], template("index.html", posts=items or "<li>Nothing yet.</li>", updated=updated))
    )

    base = SITE["url"].rstrip("/")
    feed_items = "".join(
        f"<item><title>{escape(p['title'])}</title>"
        f"<link>{base}/writing/{p['slug']}/</link>"
        f"<guid>{base}/writing/{p['slug']}/</guid>"
        f"<pubDate>{format_datetime(p['date'].replace(tzinfo=timezone.utc))}</pubDate>"
        f"<description>{escape(p['body'])}</description></item>"
        for p in posts[:20]
    )
    (OUT / "feed.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0"><channel>'
        f"<title>{escape(SITE['title'])}</title><link>{base}/</link>"
        f"<description>{escape(SITE['description'])}</description>{feed_items}"
        "</channel></rss>\n"
    )

    (OUT / "404.html").write_text(page("Not found", template("404.html")))
    print(f"built {len(posts)} post(s) into _site/")


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        handler = partial(SimpleHTTPRequestHandler, directory=OUT)
        print("serving at http://localhost:8000 (ctrl-c to stop)")
        ThreadingHTTPServer(("", 8000), handler).serve_forever()
