---
title: A small static blog, built from a git repo
description: How this site is built: Markdown in git, a short Python script, and GitHub Pages.
---

I wanted somewhere to write that I could still own in twenty years. Every hosted platform I have used has either changed its terms, changed its editor, or quietly disappeared. The most durable thing I could think of was a folder of text files under version control, so that is what this site is.

Posts are Markdown files in a `posts/` directory. A short Python script turns them into HTML, and a GitHub Action runs that script and publishes the result every time I push to `main`. There is no database, no admin panel, and nothing to patch.

<figure>
<div class="diagram">
<svg class="wide" viewBox="0 0 600 110" role="img" aria-label="Markdown in git, built by GitHub Actions, served by GitHub Pages"><g fill="none" stroke="currentColor" stroke-width="1.5"><rect x="4" y="25" width="150" height="60"/><rect x="225" y="25" width="150" height="60"/><rect x="446" y="25" width="150" height="60"/><path d="M158 55h60M211 49l7 6-7 6M379 55h60M432 49l7 6-7 6"/></g><g fill="currentColor" font-family="Times New Roman, serif" font-size="17" text-anchor="middle"><text x="79" y="52">posts/*.md</text><text x="79" y="73" font-size="14">in git</text><text x="300" y="52">build.py</text><text x="300" y="73" font-size="14">GitHub Actions</text><text x="521" y="52">static HTML</text><text x="521" y="73" font-size="14">GitHub Pages</text></g></svg>
<svg class="tall" viewBox="0 0 320 250" role="img" aria-label="Markdown in git, built by GitHub Actions, served by GitHub Pages"><g fill="none" stroke="currentColor" stroke-width="1.5"><rect x="70" y="4" width="180" height="56"/><rect x="70" y="97" width="180" height="56"/><rect x="70" y="190" width="180" height="56"/><path d="M160 62v30M154 85l6 7 6-7M160 155v30M154 178l6 7 6-7"/></g><g fill="currentColor" font-family="Times New Roman, serif" font-size="17" text-anchor="middle"><text x="160" y="29">posts/*.md</text><text x="160" y="49" font-size="14">in git</text><text x="160" y="122">build.py</text><text x="160" y="142" font-size="14">GitHub Actions</text><text x="160" y="215">static HTML</text><text x="160" y="235" font-size="14">GitHub Pages</text></g></svg>
</div>
<figcaption>Figure 1. The whole pipeline. Each box is one thing I can read or replace.</figcaption>
</figure>

## Writing a post

A post is a file with a date in its name and a few lines of front matter. That is the entire authoring interface:

```
---
title: A small static blog, built from a git repo
---

I wanted somewhere to write that I could still own...
```

Drafts get `draft: true` and stay out of the build. Images go in the `images/` folder and show up with ordinary Markdown, like `![A photo](/images/desk.jpg)`.

## Why it looks like 1998

Pages from the late nineties loaded instantly, printed cleanly, and are still readable today. Most of that came from having almost nothing on the page. So the stylesheet here sets a column width, a font size, and a dark mode, and leaves the rest to the browser.

## What I would add next

Probably tags, and a plain-text version of each post for anyone reading in a terminal. Probably not comments.
