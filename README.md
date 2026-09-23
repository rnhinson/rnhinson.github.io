# rnh.bio

Source for [rnh.bio](https://rnh.bio). Posts are Markdown files in `posts/`; pushing to
`main` builds the site with `build.py` and deploys it to GitHub Pages.

## Writing

Create `posts/YYYY-MM-DD-slug.md`:

```
---
title: Post title
description: One line for search results and link previews (optional).
draft: false
---

Markdown here.
```

The post is published at `/writing/slug/`. Images go in `images/` and are referenced as
`/images/name.jpg`. Set `draft: true` to keep a post out of the build.

## Local preview

```
pip install -r requirements.txt
python build.py --serve
```

## Settings

`site.toml` holds the site title, URL, description, GitHub username, and an optional email.
