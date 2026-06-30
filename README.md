# CML Statistical Analysis — Course Notes

Jupyter Book accompanying the *CML Statistical Analysis* training session at the API Inspection and Mechanical Integrity Summit.

**Live site:** https://sgauspohl3.github.io/CML-Statistics/

## Structure

Two parts:

**Front Matter**
- Foreword
- Introduction and Setup

**Course**
1. Statistics Refresher
2. Inspection Data and Analysis
3. Frequentist Statistical Analysis
   - 3a. Example — Frequentist CML Analysis
4. Bayesian Statistical Analysis
   - 4a. Example — Bayesian CML Analysis
5. Discussion and References

## Build locally

```bash
pip install "jupyter-book<2"
pip install -r requirements.txt
jupyter-book build .
open _build/html/index.html        # macOS
xdg-open _build/html/index.html    # Linux
```

## Edit

- **Content** lives in `intro.md` (preface), `chapters/foreword.md`, and the numbered chapter files.
- **Structure** (sidebar order, parts) is in `_toc.yml`.
- **Settings** (title, theme, repo URL) are in `_config.yml`.
- **References** go in `references.bib`; cite inline with `` {cite}`key` ``.

## Deploy

The included `.github/workflows/deploy.yml` rebuilds and publishes the site on every push to `main`. Make sure GitHub Pages → Source is set to **GitHub Actions** in repo settings.

## Useful Jupyter Book features

- **Admonitions:** `` ```{note} ``, `` ```{warning} ``, `` ```{tip} ``, `` ```{important} ``, `` ```{epigraph} ``
- **Math:** inline `$...$`, display `$$...$$`
- **Citations:** `` {cite}`bibkey` ``
- **Cross-references:** `[](section-label)` after defining `(section-label)=`
