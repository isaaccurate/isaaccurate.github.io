# Portfolio

My personal portfolio, built with Jekyll and al-folio for GitHub Pages.

## Local preview

Requires Ruby 3.3+ and Bundler. First-time setup:

```sh
bundle config set --local path vendor/bundle
bundle install
```

Start the site with `./scripts/dev.sh`, then open [localhost:4000](http://localhost:4000/). Refresh after edits; restart after changing `_config.yml`.

## Editing

- `index.html` — About
- `_data/` — profile, contact links, navigation, and coursework
- `_projects/` — project cards; `repository` sets each title’s GitHub link
- `_knowledge/` and `_posts/` — notes and blog posts
- `assets/css/portfolio.css` — styling
- `_layouts/` and `_includes/` — shared page structure and components

Content starters are in `templates/`. For exporting selected vault notes, see [Obsidian workflow](docs/OBSIDIAN.md).

For equations, set `math: true` in a note’s front matter. Use `$$...$$` inline, or put the `$$` delimiters on separate lines with blank lines around the block for display equations. MathJax loads only on those pages.

## Deployment

Set `url` and `baseurl` in `_config.yml`. Use an empty `baseurl` for a root site, or `/repository-name` for a project site. In the GitHub repository’s **Settings → Pages**, select **GitHub Actions**. Pushing to `main` runs the build, checks, and deployment in `.github/workflows/pages.yml`.

## Credits

Based on [al-folio](https://github.com/alshedivat/al-folio) by Maruan Al-Shedivat and contributors, using `al_folio_core`. Powered by [Jekyll](https://jekyllrb.com/), with custom layouts, styling, and content tools for this site. The original MIT license notice is retained in [LICENSE](LICENSE).
