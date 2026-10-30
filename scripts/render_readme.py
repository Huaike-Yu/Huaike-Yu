"""Render the academic profile from public, explicitly sourced data (Python 3.10+)."""

from collections import Counter
from html import escape
from pathlib import Path
from urllib.parse import urlencode
import json


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = ROOT / "data"
GROUPS = [
    ("Image watermarking", ["push-pull", "one-prompt", "disentangle-drop", "survey"]),
    ("Steganography", ["style-cover"]),
    ("Large language model security", ["llm-security"]),
]


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def valid_count(value):
    return value is None or (type(value) is int and value >= 0)


def scholar_search(title=None):
    if title:
        return "https://scholar.google.com/scholar?" + urlencode({"q": '"' + title + '"'})
    return "https://scholar.google.com/citations?" + urlencode(
        {"view_op": "search_authors", "mauthors": "Huaike Yu", "hl": "en"}
    )


def picture(light, dark, alt, width):
    return f'''<picture>
    <source media="(prefers-color-scheme: dark)" srcset="{escape(dark, quote=True)}">
    <source media="(prefers-color-scheme: light)" srcset="{escape(light, quote=True)}">
    <img alt="{escape(alt, quote=True)}" src="{escape(light, quote=True)}" width="{width}">
  </picture>'''


def scholar_card(scholar, dark=False):
    bg, ink, muted, line, accent = (
        ("#101827", "#edf2fc", "#a9b9d4", "#2e3f58", "#b4a2ed")
        if dark else ("#f7f8fc", "#17243c", "#526580", "#d8e1ef", "#7a69ae")
    )
    labels = [("citations", "CITATIONS"), ("h_index", "H-INDEX"), ("i10_index", "I10-INDEX")]
    cells = []
    for index, (key, label) in enumerate(labels):
        value = scholar["metrics"].get(key)
        number = "—" if value is None else f"{value:,}"
        x = 28 + index * 140
        cells.append(f'<text x="{x}" y="109" font-size="36" fill="{ink}">{number}</text>')
        cells.append(f'<text x="{x}" y="134" font-size="11" letter-spacing="1.3" fill="{muted}">{label}</text>')
    date = scholar.get("updated")
    foot = f"All-time metrics · checked {date}" if date else "Profile link pending · — means unverified"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="195" viewBox="0 0 460 195" role="img" aria-labelledby="title desc">
<title id="title">Google Scholar metrics</title><desc id="desc">{escape(foot)}. Citations, h-index and i10-index.</desc>
<rect x="0.5" y="0.5" width="459" height="194" rx="12" fill="{bg}" stroke="{line}"/>
<g font-family="Arial,Helvetica,sans-serif"><text x="28" y="37" font-size="19" font-weight="600" fill="{accent}">Google Scholar</text>
{''.join(cells)}
<path d="M166 75v63M306 75v63" stroke="{line}"/>
<text x="28" y="174" font-size="11" fill="{muted}">{escape(foot)}</text></g></svg>'''


def initials(name):
    parts = name.split()
    return " ".join(part[0] + "." for part in parts[:-1]) + " " + parts[-1]


def publication(paper, scholar, own_name):
    record = scholar.get("papers", {}).get(paper["id"], {})
    value = record.get("citations")
    citation = "—" if value is None else str(value)
    authors = ", ".join(
        f"<strong>{escape(name)}</strong>" if name == own_name else escape(initials(name))
        for name in paper["authors"]
    )
    citation_url = record.get("cited_by_url")
    citation_label = f'<a href="{escape(citation_url, quote=True)}">Cited by {citation}</a>' if citation_url else f"Citations: {citation}"
    search = scholar_search(paper["title"])
    venue = paper["venue"]
    return f'''<p>
  <strong><a href="{escape(paper['url'], quote=True)}">{escape(paper['title'])}</a></strong><br>
  <sub>{authors}</sub><br>
  <sub>{paper['year']} · {escape(paper['status'])} · {escape(venue)} &nbsp; / &nbsp; {citation_label} · <a href="{escape(search, quote=True)}">Scholar</a></sub>
</p>'''


def main():
    profile = json.loads((DATA / "profile.json").read_text(encoding="utf-8"))
    scholar = json.loads((DATA / "scholar.json").read_text(encoding="utf-8"))
    for value in scholar["metrics"].values():
        assert valid_count(value), "Citation metrics must be nonnegative integers or null."
    if any(value is not None for value in scholar["metrics"].values()):
        assert scholar.get("profile_url") and scholar.get("updated"), "Scholar metrics require a source and check date."
    for record in scholar.get("papers", {}).values():
        assert valid_count(record.get("citations"))
        if record.get("citations") is not None:
            assert record.get("source_url") and record.get("updated"), "Paper counts require a source and check date."

    papers = {paper["id"]: paper for paper in profile["publications"]}
    grouped_ids = [key for _, keys in GROUPS for key in keys]
    assert len(grouped_ids) == len(set(grouped_ids)) and set(grouped_ids) == set(papers)

    for dark in (False, True):
        write(ASSETS / f"scholar-{'dark' if dark else 'light'}.svg", scholar_card(scholar, dark))
    write(ASSETS / "scholar.svg", '''<svg xmlns="http://www.w3.org/2000/svg" width="145" height="30" viewBox="0 0 145 30" role="img" aria-label="Google Scholar"><rect x=".5" y=".5" width="144" height="29" rx="5" fill="#17243c" stroke="#43526c"/><path d="m10 12 8-5 8 5-8 5Zm3 3v5c3 2 7 2 10 0v-5M26 12v8" fill="none" stroke="#c6b6f2" stroke-width="1.4" stroke-linejoin="round"/><text x="35" y="19.5" fill="#f2f5fc" font-family="Arial,Helvetica,sans-serif" font-size="12.5">Google Scholar</text></svg>''')

    sections = []
    for title, keys in GROUPS:
        sections.append(f"### {title}\n\n" + "\n\n".join(publication(papers[key], scholar, profile["name"]) for key in keys))

    coauthors = Counter()
    for paper in profile["publications"]:
        coauthors.update(name for name in dict.fromkeys(paper["authors"]) if name != profile["name"])
    frequent = coauthors.most_common(8)
    coauthor_rows = "\n".join(f"| {name} | {count} |" for name, count in frequent)
    remaining = " · ".join(name for name, _ in coauthors.most_common()[8:])
    education = "\n".join(f"- **{item['institution']}** — {item['degree']} ({item['period']})." for item in profile["education"])

    stats = "https://github-stats-extended.vercel.app/api?" + urlencode({
        "username": "Huaike-Yu", "show_icons": "true", "hide_rank": "true", "hide_border": "false",
        "custom_title": "GitHub activity", "hide": "contribs", "title_color": "7a69ae", "icon_color": "7a69ae",
        "text_color": "526580", "bg_color": "f7f8fc", "border_color": "d8e1ef", "border_radius": "12",
    })
    dark_stats = stats.replace("7a69ae", "b4a2ed").replace("526580", "a9b9d4").replace("f7f8fc", "101827").replace("d8e1ef", "2e3f58")
    scholar_url = scholar.get("profile_url") or scholar_search()
    scholar_picture = picture("./assets/scholar-light.svg", "./assets/scholar-dark.svg", "Google Scholar citation metrics; unverified values are shown as dashes", 460)
    stats_picture = picture(stats, dark_stats, "Huaike-Yu's GitHub activity: stars, commits, pull requests and issues", 400)
    if scholar.get("profile_url"):
        scholar_picture = f'<a href="{escape(scholar_url, quote=True)}">{scholar_picture}</a>'
    scholar_note = (
        f"Google Scholar all-time metrics and paper counts checked {scholar['updated']}."
        if scholar.get("updated") else
        "Google Scholar profile link is being confirmed; unverified citation metrics are shown as —."
    )
    view_url = "https://komarev.com/ghpvc/?username=Huaike-Yu&label=Profile+views&color=7a69ae&style=flat-square"
    star_base = "https://img.shields.io/github/stars/Huaike-Yu/"
    star_style = "?style=flat-square&label=Stars&color=7a69ae&labelColor=17243c"
    email = profile["email"].replace("@", "[at]")
    readme = f'''<!-- Layout inspired by awesome-github-profile-readme; original header and Scholar artwork. Generated by scripts/render_readme.py. -->
<h1>
  {picture('./assets/academic-header-light.svg', './assets/academic-header-dark.svg', 'Huaike Yu — Image Watermarking, Steganography, and AI Security', 1200)}
</h1>

<p>
  <a href="https://huaike-yu.github.io/"><img src="./assets/homepage.svg" alt="Academic homepage" height="28"></a>
  <a href="{escape(scholar_url, quote=True)}"><img src="./assets/scholar.svg" alt="Google Scholar{' profile' if scholar.get('profile_url') else ' author search'}" height="28"></a>
  <a href="https://huaike-yu.github.io/assets/Huaike_Yu_CV.pdf"><img src="./assets/cv.svg" alt="Curriculum vitae" height="28"></a>
  <a href="#research-by-topic"><img src="./assets/publications.svg" alt="Research by topic" height="28"></a>
</p>

<p>
  <strong>Research Assistant</strong> at <strong>Qilu University of Technology (Shandong Academy of Sciences)</strong>.<br>
  Research guidance: <strong>Qi Li</strong> &nbsp; · &nbsp; Email: <code>{email}</code>
</p>

My research focuses on **invisible image watermarking**, **steganography**, and **AI security**.

## Research overview

{scholar_picture}

<sub>{scholar_note} The six works below include five preprints and one published article.</sub>

## Research by topic

{(chr(10) * 2).join(sections)}

## Collaborators

Coauthorship across the **{len(papers)} works listed here** · **{len(coauthors)} collaborators**.

| Frequent coauthor | Shared works |
| :-- | --: |
{coauthor_rows}

<details>
<summary><strong>Other coauthors</strong></summary>

{remaining}

</details>

## GitHub & open source

<a href="https://github.com/Huaike-Yu">{stats_picture}</a>

| Repository | Focus | Stars |
| :-- | :-- | :-- |
| [Academic website](https://github.com/Huaike-Yu/Huaike-Yu.github.io) | Personal academic homepage & CV | [![Website stars]({star_base}Huaike-Yu.github.io{star_style})](https://github.com/Huaike-Yu/Huaike-Yu.github.io/stargazers) |
| [Academic profile](https://github.com/Huaike-Yu/Huaike-Yu) | Research overview & publications | [![Profile repository stars]({star_base}Huaike-Yu{star_style})](https://github.com/Huaike-Yu/Huaike-Yu/stargazers) |

![Profile views]({view_url})

<sub>GitHub cards and Stars are refreshed by their badge providers. Profile views is an approximate badge-load counter since installation; repeat loads may count.</sub>

## Background & methods

Master’s Degree in **Simulation and Immersive Technologies**, **UNSW** (February 2024 – August 2025).

<p>
  <strong>Python</strong> · <strong>Machine Learning</strong> · <strong>Deep Learning</strong> · <strong>Data Analysis</strong><br>
  Quantitative and qualitative research · Regression · Classification · Forecasting
</p>

<details>
<summary><strong>Full education</strong></summary>

{education}

</details>

---

[Academic homepage](https://huaike-yu.github.io/) &nbsp; · &nbsp; [Google Scholar]({scholar_url}) &nbsp; · &nbsp; [CV](https://huaike-yu.github.io/assets/Huaike_Yu_CV.pdf)
'''
    write(ROOT / "README.md", readme)
    print(f"Rendered {len(papers)} works in {len(GROUPS)} topics; {len(coauthors)} unique coauthors.")


if __name__ == "__main__":
    main()
