# The World in One Day — Tuesday 17 November 2026

[![news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/maezageryan-del/news-image-17nov/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard)
[![reward](https://make.fun/badge/news-image-20261117/maezageryan-del/news-image-17nov/reward.svg)](https://make.fun/bounty/news-image-20261117)

One square page, 1024 × 1024, that carries a whole day of world news the way a
broadsheet front page used to: a lead story up top, a map that shows where the
day happened, columns and a grid of shorter reports, and a strip of one-line
items along the bottom. Everything on the page happened on **Tuesday,
17 November 2026**, drawn from the reporting of BBC, Reuters, AP and
Al Jazeera.

Entry for the make.fun bounty
[news-image-20261117](https://make.fun/bounty/news-image-20261117) — see the
[leaderboard](https://make.fun/bounty/news-image-20261117/leaderboard).

## What's on the page

**The lead.** Ukraine hits the Kerch Bridge — a road span collapses. Kyiv's
strike, the second in under a day, severs the link to occupied Crimea, and
Russia answers with missiles on Kyiv's bridges over the Dnipro.

**The map band.** A dotted world map built from Natural Earth country
boundaries, with nine numbered places marking where the day's main stories
sit:

| # | Place | # | Place | # | Place |
|---|-------|---|-------|---|-------|
| 1 | Kerch Bridge | 4 | Bahrain | 7 | Tallinn |
| 2 | Kyiv | 5 | Manila | 8 | Kigali |
| 3 | Hormuz | 6 | Shenzhen | 9 | Tokyo |

**Three column stories.**

- *Middle East* — **Tankers hit by mines off Hormuz.** Iran says two tankers
  struck mines and caught fire; a third US carrier reaches the region.
- *Asia-Pacific* — **Trump lands in Manila; Xi, Putin talks set.** China
  confirms the first Xi–Trump–Putin meeting, Thursday in Shenzhen on APEC's
  sidelines.
- *Europe* — **Estonia to shut every crossing with Russia.** Tallinn cites a
  foiled Russian plot to bomb a drone plant; the border closes on 1 December.

**The six-story grid.**

- *Middle East* — Iran fires drones at a US radar site in Bahrain.
- *Americas* — JPMorgan blames a bug, not hackers, for outage.
- *Tech · Space* — Vulcan rocket fails; 40 Amazon satellites lost.
- *Americas* — Nvidia reports after Huang's exit.
- *Europe* — Five nations plan a Rwanda deportation hub.
- *Asia-Pacific* — Japan scrambles jets at Russian planes.

**Also today.** A fifteen-item strip of one-liners runs along the bottom: the
Pentagon failing its audit for a ninth year, the US curbing an AI-chip
loophole, measles cases at a 1991 high, Houthi drones hitting a Saudi oil
pipeline, Modi proposing free e-visas at ASEAN, Amazon investing $7bn in
India's renewables, India's GDP growth seen at 7.5%, and eight more.

Count them and the page holds **25 stories across five regions** — Europe,
the Middle East, Asia-Pacific, the Americas, and tech & space.

## The day at a glance

| Part of the page | Pieces | What it does |
|---|---|---|
| Lead | 1 story | the day's biggest development, above everything else |
| Map band | 9 markers | shows where the placed stories happened |
| Columns | 3 stories | the next tier down, one story per region |
| Grid | 6 stories | shorter reports, three across and two down |
| Also today | 15 one-liners | everything else that mattered, in a single strip |

Of the ten placed stories (the lead, the three columns and the six grid
reports), Europe takes three, the Middle East and Asia-Pacific two each, the
Americas two, and tech & space one. The strip then ranges wider, from a bus
crash in Uttarakhand to measles cases in the United States.

## How it was made

The page is not a screenshot or a collage; it is drawn by a program.

- `stories.json` is the day's notebook: masthead, dateline, the lead, the
  three column stories, the six grid stories, the fifteen one-liners, and the
  nine map markers with their coordinates and label offsets.
- `render.py` is the press. It reads `stories.json`, decodes a Natural Earth
  countries-110m TopoJSON file (passed to it as a command-line argument),
  projects the country outlines onto an equirectangular dotted map, and then
  composes the whole page — masthead, lead, map band, columns, grid, strip
  and footer — onto a 1024 × 1024 canvas with Pillow.
- `entry.png` is the printed sheet: the fixed, finished front page.
  `render.py` writes `front-page.png` by default when it redraws the page,
  so a re-render can never overwrite the shipped `entry.png` by accident.
- `main.ts` is the entrypoint the bounty runs. It takes the finished
  `entry.png` sitting next to it and delivers a copy to
  `$MAKEFUN_OUTPUT_DIR/entry.png`, checking on the way that the source exists
  and that the copy arrived whole.

To redraw the page from the notebook:

```sh
python3 render.py countries-110m.json   # writes a fresh front page image
```

## Why a front page

A feed gives every story the same size and lets the day dissolve into a
scroll. A front page forces judgement: one story leads, a map shows the
shape of the day at a glance, and everything else has to earn its column
inches. This entry squeezes that discipline into a single square image — the
whole world, one day, one page.

## License

MIT — see `LICENSE`.
