# Yukang Jiang — academic homepage

A single self-contained `index.html` (all CSS/JS/SVG inline). The only external
files are the profile photo and the citation-updater automation.

```
academic-homepage/
├── index.html                         # the whole site
├── images/yukang.jpg                  # profile photo (About section)
├── scripts/update_citations.py        # weekly Scholar citation refresher
└── .github/workflows/update-citations.yml
```

## Change the photo

Replace `images/yukang.jpg` with any portrait image of the same name and
refresh. (A tall/portrait photo fits the About sidebar frame best.)

## Deploy to GitHub Pages

1. Create a repo and push this folder to the `main` branch.
2. **Settings → Pages →** Source: *Deploy from a branch*, Branch: `main` / `root`.
3. Your site goes live at `https://<username>.github.io/<repo>/`.

## Weekly citation auto-update

`.github/workflows/update-citations.yml` runs every **Monday 06:00 UTC** (and
can be run by hand from the **Actions** tab → *Run workflow*). It reads the
Google Scholar citation total and, if it changed, commits the new number into
`index.html`. Only the `Citations` stat is touched.

**To turn it on after pushing to GitHub:**

- **Settings → Actions → General → Workflow permissions →** *Read and write
  permissions* (so the job can commit the updated number back).
- That's it — it now runs weekly using the free `scholarly` library.

**For reliable updates (recommended):** Google Scholar frequently blocks the
free GitHub runners, so the keyless `scholarly` path may skip some weeks (it
never breaks the page — it just leaves the old number). For rock-solid weekly
updates, add a free [SerpAPI](https://serpapi.com) key (free tier: 100
searches/month; this uses ~4):

- **Settings → Secrets and variables → Actions → New repository secret**
  - Name: `SERPAPI_KEY`  Value: *your SerpAPI key*

The script prefers SerpAPI when the secret is present, and falls back to
`scholarly` otherwise.

> Note: GitHub disables scheduled workflows after ~60 days with no repository
> activity. The weekly commit normally keeps it awake, but if it ever pauses,
> just re-enable it in the Actions tab.
