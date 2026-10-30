# Profile data and metrics

Edit `data/profile.json` for profile details and publications, then run:

```sh
python scripts/render_readme.py
```

## Google Scholar

`data/scholar.json` stores an explicitly checked snapshot. Set `profile_url` to
the confirmed public Google Scholar profile and `updated` to the check date
(`YYYY-MM-DD`). `metrics.citations`, `h_index` and `i10_index` are all-time values
from that profile. Each paper has its own citation count, source URL and check
date. A `cited_by_url` can link directly to its citing papers.

Unknown values are `null` and render as **—**, not zero. A verified zero is the
integer `0`. The renderer rejects counts with no source/check date. No automatic
Scholar scraping is configured. Until the author profile is confirmed, the
navigation opens an author search, and individual paper links open title searches.

Do not add the paper counts together to infer Scholar's profile total or derive
h-index/i10-index from a partial publication list. Preserve the source's own values.

## Coauthorship

Coauthor counts are calculated from the six supplied publication records,
excluding Huaike Yu. Each person is counted once per work. These counts describe
the included records, rather than a complete Google Scholar collaboration graph.
Author order is preserved on each paper; the profile owner's name is bold.

## GitHub statistics and Stars

The GitHub activity card uses
[GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended).
It uses public GitHub activity and requires no token in this repository. It is
provided in both light and dark themes. Commit counts use the card's stated period.
Repository Stars use [Shields.io](https://shields.io/badges/git-hub-repo-stars)
and link to each repository's stargazers. Provider/GitHub image caching may delay
updates; a temporary provider outage may affect these external images.

Only the two currently public repositories are featured. Add future released
research repositories explicitly in `scripts/render_readme.py` when available.

## Profile views

The badge uses [GitHub Profile Views Counter](https://github.com/antonkomarev/github-profile-views-counter).
It starts counting loads when installed, with no artificial base value. Repeated
loads, previews, proxies and caching affect the count. It is an approximate
badge-load counter, not historical GitHub page traffic or unique visitors.
