# Deliberate publishing from Obsidian

The vault is private source material, not a deployment dependency. Keep it outside this repository. The sync script creates a small, reviewable export; GitHub Actions only receives those exported files.

## Setup

Requires Python 3.10+. From the portfolio repository:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

To check the exporter after changes, run `.venv/bin/python -m unittest discover -s tests -v`.

## Folder contract

Inside your external vault, create:

```text
Publish/        Only notes eligible for consideration
PublishAssets/  Only attachments cleared for public use
```

Change these relative names in `obsidian-sync.yml` if necessary. The script does not resolve arbitrary vault paths, copy the entire asset directory, or chase links into private notes. Symlinks escaping approved folders are rejected. Never place secrets in the publication folders or repository.

## Note contract

Copy `templates/obsidian-note.md` into `Publish/`. Required fields for an opted-in note:

```yaml
---
publish: true
slug: regularization-checklist
title: A regularization checklist
description: How I compare model complexity without touching the test set.
date: 2026-10-30
tags: [nlp, evaluation]
categories: [machine-learning]
---
```

`publish` must be the YAML boolean `true`, not the string `"true"`. Slugs must be unique lowercase words separated by hyphens. Only title, description, date, tags, and categories are exported; layout/permalink and arbitrary metadata never pass through. The generated `kind` is Technical note.

Everything in an opted-in note's body is intended for public reading. The script is a selection and conversion tool, **not a secret detector**. Review prose, code samples, external links, and attachments yourself. Raw HTML, Liquid, private Obsidian comments, and HTML comments stop the sync for manual review.

## Links and assets

- `[[Other Note]]` and `[[Other Note|Readable label]]` resolve only to another opted-in note. Use a path relative to `Publish/` or the vault if names collide.
- Every wikilink must resolve uniquely; links to private/unselected/missing notes stop the entire sync before files are written.
- `![[diagram.png|A useful description]]` copies a referenced attachment from `PublishAssets/`, gives it a content-hashed filename, and emits a baseurl-aware Jekyll image link.
- Standard `![Description](diagram.png)` uses the same attachment allowlist. For subfolders use `diagrams/flow.png`, relative to `PublishAssets/`.
- PNG, JPG, JPEG, GIF, WebP, and PDF are supported. PDFs become download links. SVG, HTML, and executable formats are deliberately excluded. A PNG/JPG/PDF may still contain identifying information or metadata; review it.
- Image captions must be descriptive text, not Obsidian size shortcuts such as `300` or `300x200`.
- External standard Markdown links use `https://`, `http://`, or `mailto:`; same-page `#anchors` are supported.
- Heading/block wikilinks, transclusions of notes, Canvas, Dataview, reference-style links, and arbitrary relative Markdown links require manual conversion. The exporter is deliberately conservative; even wikilink-looking text in code blocks is subject to validation. For such notes, author a reviewed native Jekyll note directly in `_knowledge/`.

All planned conversions validate before any write. A disk failure during writes can still leave a partial export; inspect the diff before committing.

## Publish and review

```sh
.venv/bin/python scripts/sync_obsidian.py --vault '/absolute/path/to/vault' --dry-run
.venv/bin/python scripts/sync_obsidian.py --vault '/absolute/path/to/vault'
git diff -- _knowledge assets/notes .obsidian-sync-manifest.json
bundle exec jekyll serve
```

The dry run validates without writing. The real sync emits only selected notes and referenced attachments. Review the full diff, including any new files shown by `git status`, then commit the generated Markdown, assets, and `.obsidian-sync-manifest.json`. The manifest contains output paths/hashes, never absolute vault paths. Do not edit generated notes in the repository; change the vault source. Hash checks protect manually changed generated files from silent overwrite/deletion.

## Unpublish

Change `publish: true` to `false` or move the note outside `Publish/`, then rerun sync. Old generated notes and no-longer-referenced attachments are removed using the manifest. Any remaining public note linking to it must first be updated. Review and push the removals.

Removing a page from the current site does not remove it from Git history, previous deployments, downloads, or search caches. For accidental exposure, remove the published content promptly and handle history/cache cleanup separately.

## Automation choice

This repository intentionally automates **validation and deployment**, not access to the private vault. A local manual sync gives a review point before public publication. GitHub's hosted runners cannot see your local Obsidian vault; do not upload the full vault or add it as an Actions artifact to solve that.

If you later need unattended sync, use a dedicated public-only export repository and a locally controlled job that opens a review branch. Scope credentials to that export repository, keep the private vault local, and require a review before merging. No such job or credentials are installed here.
