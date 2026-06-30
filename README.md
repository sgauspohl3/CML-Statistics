# Introduction to Statistics — Course Notes

A Jupyter Book of undergraduate statistics notes.

**Live site:** https://github.com/sgauspohl3/CML-Statistics.git *(after you deploy)*

## Build locally

```bash
pip install -r requirements.txt
jupyter-book build .
open _build/html/index.html        # macOS
xdg-open _build/html/index.html    # Linux
```

## Edit

- **Content** lives in `intro.md` and `chapters/*.md`.
- **Structure** (sidebar order) is defined in `_toc.yml`.
- **Settings** (title, theme, repo URL, math macros) are in `_config.yml`.
- **References** go in `references.bib`; cite inline with `` {cite}`key` ``.

To add a new chapter:

1. Create `chapters/your_new_chapter.md`.
2. Add `- file: chapters/your_new_chapter` to `_toc.yml` under the right part.
3. Rebuild.

## Deploy to GitHub Pages

### One-time setup

1. Create a public GitHub repo (e.g. `intro-statistics`).
2. Update the `repository.url` field in `_config.yml` with your repo URL.
3. Push this folder:

   ```bash
   git init
   git add .
   git commit -m "initial book"
   git branch -M main
   git remote add origin https://github.com/sgauspohl3/CML-Statistics.git
   git push -u origin main
   ```

4. In the repo on GitHub: **Settings → Pages → Source: GitHub Actions**.

### Automatic deploys

The included `.github/workflows/deploy.yml` rebuilds and publishes the site on every push to `main`. After a successful run, visit:

```
https://github.com/sgauspohl3/CML-Statistics.git
```

## Switching code blocks to executable notebooks

The `.md` files use fenced ```` ```{code-cell} python ```` blocks. These render as syntax-highlighted code by default. To execute them and embed plot outputs:

1. Convert the `.md` to a `.ipynb` (or use [MyST notebooks](https://jupyterbook.org/en/stable/file-types/myst-notebooks.html) with a YAML header).
2. Set `execute_notebooks: auto` in `_config.yml`.

## Useful Jupyter Book features

- **Admonitions:** `` ```{note} ``, `` ```{warning} ``, `` ```{tip} ``, `` ```{important} ``
- **Math:** inline `$...$`, display `$$...$$`
- **Cross-references:** `[](section-label)` after defining `(section-label)=`
- **Citations:** `` {cite}`bibkey` ``
- **Hidden code cells:** add `:tags: [hide-input]` after the fence
