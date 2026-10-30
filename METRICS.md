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
Scholar scraping is configured. The profile navigation and metric card link to
[Huaike Yu's confirmed profile](https://scholar.google.com/citations?hl=zh-CN&user=GN3ipIUAAAAJ).
Individual paper links open their Scholar records; positive counts link directly
to the citing papers.
Generated metric images use a content hash in their filenames, so a changed
snapshot receives a fresh image URL instead of reusing GitHub's cached image.

The 2026-10-30 snapshot contains all six rows shown in this profile: 8 citations,
h-index 1 and i10-index 0. The LLM-security article has 7 citations and One Prompt
has 1. The remaining four citation cells are blank in Scholar and are recorded
as zero at this check. The source profile showed articles 1–6 with no more rows.

Do not add the paper counts together to infer Scholar's profile total or derive
h-index/i10-index from a partial publication list. Preserve the source's own values.

## Coauthorship

Coauthor counts are calculated from the six supplied publication records,
excluding Huaike Yu. Each person is counted once per work. These counts describe
the included records, rather than a complete Google Scholar collaboration graph.
Author order is preserved on each paper; the profile owner's name is bold.
The four coauthor profile links in `data/scholar.json` were verified from the
profile's own coauthor sidebar on 2026-10-30. Other names remain plain text.

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
