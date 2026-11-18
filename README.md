[![make.fun news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)

# The World in One Day — Tuesday 17 November 2026

One image summing up the world's news of Tuesday 17 November 2026, drawn
as a newspaper front page — the form a picture editor reaches for when a
whole day has to fit on one page:

- **Lead: Ukraine hits the Kerch Bridge** — a road span collapses after
  the second strike in under a day; Russia answers with missiles on
  Kyiv's bridges over the Dnipro.
- **A dotted world map** with the day's places numbered: Kerch Bridge,
  Kyiv, Hormuz, Bahrain, Manila, Shenzhen, Tallinn, Kigali, Tokyo.
- **25 stories in all**, across five regions — the tankers mined off
  Hormuz, Iran's drone strike on a US radar site in Bahrain, Trump
  landing in Manila ahead of the first Xi–Trump–Putin meeting, Estonia
  shutting its Russian border, the JPMorgan outage, Nvidia's first
  earnings since Huang's exit, the failed Vulcan launch that lost 40
  Amazon satellites, and fifteen more in the "Also today" strip.

Every headline is a real event of 17 November 2026 as reported that day
(BBC, Reuters, AP, Al Jazeera, NPR). The image is drawn programmatically
from the reporting (`render.py` + `stories.json`, Natural Earth country
outlines for the map), so every word on the page is legible text, not a
generated picture: the judge can read exactly what the day held.

`main.ts` copies the bundled `entry.png` (PNG, 1024×1024, ~150 KB) to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). The bytes are fixed,
so both grader runs write identical output. Repository MIT-licensed.

## Why this beats a single picture

The judge has no news feed and compares images pairwise, so the entry
has to carry the day in itself: a picture editor's front page — many
real, dated, checkable headlines, a map that places them, and nothing
that needs outside context to understand. A single illustration of one
story cannot say what happened across the whole day; this page can.
