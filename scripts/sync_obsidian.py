#!/usr/bin/env python3
"""Explicit opt-in Obsidian publishing. Validate the whole plan before writing."""
import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote
import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / '.obsidian-sync-manifest.json'
SAFE_ASSETS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.pdf'}
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def inside(path, parent):
    path = path.resolve()
    if not path.is_relative_to(parent.resolve()):
        raise ValueError(f'Path escapes allowed folder: {path.name}')
    return path


def frontmatter(path):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', text, re.S)
    if not match:
        return None, text
    meta = yaml.safe_load(match[1])
    if not isinstance(meta, dict):
        raise ValueError(f'Front matter must be a mapping: {path.name}')
    return meta, match[2]


def sync(vault, config, destination, dry_run=False):
    vault = vault.resolve()
    cfg = yaml.safe_load(config.read_text())
    notes_dir = inside(vault / cfg['notes_dir'], vault)
    assets_dir = inside(vault / cfg['assets_dir'], vault)
    if not notes_dir.is_dir():
        raise ValueError('Configured notes_dir must exist')
    destination = inside(destination, ROOT / '_knowledge')
    selected = []
    aliases = {}
    for source in sorted(notes_dir.rglob('*.md')):
        inside(source, notes_dir)  # Reject symlinks out of the approved tree.
        if any(part.startswith('.') for part in source.relative_to(notes_dir).parts):
            continue
        meta, body = frontmatter(source)
        if not meta or meta.get('publish') is not True:
            continue
        if not all(meta.get(key) for key in ('title', 'description', 'date', 'slug')):
            raise ValueError(f'Missing title, description, date or slug: {source.name}')
        slug = meta['slug']
        if not isinstance(slug, str) or not SLUG.fullmatch(slug):
            raise ValueError(f'Invalid slug: {source.name}')
        datetime.date.fromisoformat(str(meta['date'])[:10])
        for key in ('tags', 'categories'):
            if not isinstance(meta.get(key, []), list) or not all(isinstance(x, str) for x in meta.get(key, [])):
                raise ValueError(f'{key} must be a list of strings: {source.name}')
        output = destination / f'{slug}.md'
        if any(item[3] == output for item in selected):
            raise ValueError(f'Duplicate slug: {slug}')
        selected.append((source, meta, body, output))
        for alias in {source.stem, source.relative_to(notes_dir).with_suffix('').as_posix(), source.relative_to(vault).with_suffix('').as_posix()}:
            aliases.setdefault(alias.casefold(), []).append(slug)
    assets = {}

    def asset_link(target):
        # Paths are always relative to the explicitly approved assets folder.
        target = unquote(target)
        if target.startswith(('/', '\\')) or '\\' in target or '..' in Path(target).parts:
            raise ValueError('Asset paths must be relative and cannot traverse folders')
        asset = inside(assets_dir / target, assets_dir)
        if asset.suffix.lower() not in SAFE_ASSETS or not asset.is_file():
            raise ValueError(f'Unsupported or missing attachment: {target}')
        data = asset.read_bytes()
        digest = hashlib.sha256(data).hexdigest()[:16]
        name = digest + asset.suffix.lower()
        output = ROOT / 'assets/notes' / name
        assets[output] = data
        return "{{ '/assets/notes/" + name + "' | relative_url }}"

    def wiki(match):
        embed, raw = match.groups()
        target, _, label = raw.partition('|')
        target = target.strip()
        if embed:
            url = asset_link(target)
            if not label or label.isdigit() or re.fullmatch(r'\d+x\d+', label):
                raise ValueError(f'Attachment needs descriptive alt text: {target}')
            return f'![{label}]({url})' if Path(target).suffix.lower() != '.pdf' else f'[{label}]({url})'
        target, _, heading = target.partition('#')
        if heading:
            raise ValueError('Heading and block wikilinks require a reviewed standard Markdown link')
        matches = aliases.get(target.removesuffix('.md').casefold(), [])
        if len(matches) != 1:
            raise ValueError(f'Wikilink target must resolve to exactly one published note: {target}')
        url = "{{ '/knowledge/" + matches[0] + "/' | relative_url }}"
        return f'[{label or target}]({url})'

    old = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {'files': {}}
    old_files = old['files']
    planned = {}
    for source, meta, body, output in selected:
        # Prohibit raw HTML/Liquid and Obsidian private comments; Markdown is the supported contract.
        if re.search(r'\{%|\{\{|<!--|%%|<\/?[A-Za-z]', body):
            raise ValueError(f'Raw HTML, Liquid, or private comments require manual review: {source.name}')
        # Convert approved Markdown image attachments before wikilinks; other local links are rejected.
        def markdown_asset(match):
            label, target = match.groups()
            if target.startswith(('https://', 'http://')):
                return match[0]
            if not label.strip():
                raise ValueError('Images need descriptive alt text')
            return f'![{label}]({asset_link(target)})'
        body = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', markdown_asset, body)
        # Existing standard links may be HTTPS, HTTP, mailto, or same-page anchors only.
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', body):
            if not target.startswith(('https://', 'http://', 'mailto:', '#')):
                raise ValueError(f'Use a wikilink for published notes or an absolute public link: {source.name}')
        if re.search(r'^\s*\[[^\]]+\]:', body, re.M):
            raise ValueError('Reference-style links need manual review')
        body = re.sub(r'(!?)\[\[([^\]]+)\]\]', wiki, body)
        # Never pass through arbitrary front matter (permalink, layout, publish controls, etc.).
        clean = {key: meta[key] for key in ('title', 'description', 'date', 'tags', 'categories') if key in meta}
        clean['kind'] = 'Technical note'
        planned[output] = ('---\n' + yaml.safe_dump(clean, sort_keys=False, allow_unicode=True) + '---\n' + body).encode()
    planned.update(assets)
    # Generated files are managed by hash: never overwrite/delete hand edits silently.
    for name, digest in old_files.items():
        path = inside(ROOT / name, ROOT)
        if not (path.is_relative_to(destination) or path.is_relative_to(ROOT / 'assets/notes')):
            raise ValueError('Manifest contains an unmanaged path')
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f'Generated file was edited; resolve before syncing: {name}')
    for output, data in planned.items():
        rel = output.relative_to(ROOT).as_posix()
        if output.exists() and rel not in old_files and output.read_bytes() != data:
            raise ValueError(f'Refusing to overwrite an unmanaged file: {rel}')
    stale = [ROOT / name for name in old_files if ROOT / name not in planned]
    print(f'{len(selected)} opted-in notes, {len(assets)} referenced assets, {len(stale)} stale files; ' + ('dry run' if dry_run else 'sync'))
    if dry_run:
        return
    for output, data in planned.items():
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
    for path in stale:
        path.unlink(missing_ok=True)
    manifest = {'files': {p.relative_to(ROOT).as_posix(): hashlib.sha256(data).hexdigest() for p, data in planned.items()}}
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', required=True, type=Path)
    parser.add_argument('--config', type=Path, default=ROOT / 'obsidian-sync.yml')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        sync(args.vault, args.config, ROOT / '_knowledge', args.dry_run)
    except (ValueError, KeyError, OSError, yaml.YAMLError) as exc:
        parser.exit(1, f'Sync stopped before publishing: {exc}\n')


if __name__ == '__main__':
    main()
