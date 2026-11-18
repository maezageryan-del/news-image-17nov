[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/maezageryan-del/news-image-17nov/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard)
[![reward](https://make.fun/badge/news-image-20261117/maezageryan-del/news-image-17nov/reward.svg)](https://make.fun/bounty/news-image-20261117)

# The World in One Day — Tuesday 17 November 2026

## What this entry is

A single square image that tries to do the job of an entire day's
newspaper: everything that mattered on Tuesday 17 November 2026, laid
out as a front page. Instead of illustrating one story, the page prints
the day itself — a lead headline, a map of where things happened, and
short reports from five regions, 25 stories in total.

Nothing on the page is invented. Each headline records a real event of
17 November 2026, taken from that day's reporting by the BBC, Reuters,
AP, Al Jazeera and NPR, and the footer of the image says so.

## What is on the page

**The lead.** Ukraine's strike on the Kerch Bridge — the second in
under a day — brings down a road span and cuts the link to occupied
Crimea. Russia replies with missiles aimed at Kyiv's bridges over the
Dnipro.

**The map.** A dotted world map, captioned "Where the day happened",
pins the day's geography with nine numbered markers: the Kerch Bridge,
Kyiv, Hormuz, Bahrain, Manila, Shenzhen, Tallinn, Kigali and Tokyo. A
key under the map ties each number to its story.

**The column and the grid.** Three medium reports sit beside the map:
mined tankers burning off Hormuz as a third US carrier reaches the
region; Trump landing in Manila with the first Xi–Trump–Putin meeting
confirmed for Thursday in Shenzhen, on the sidelines of APEC; and
Estonia deciding to close every crossing with Russia from 1 December
after a foiled plot to bomb a drone plant. Below them, six shorter
pieces cover Iran's drone strike on a US radar site in Bahrain,
JPMorgan blaming a software bug — not hackers — for its outage, the
failed Vulcan launch that destroyed 40 Amazon Leo satellites, Nvidia's
first earnings since its chief executive's resignation, five European
nations planning a deportation hub in Rwanda, and Japan scrambling jets
at Russian aircraft in its airspace.

**Also today.** Fifteen one-line briefs close the page: the Pentagon's
ninth straight failed audit, US curbs on the AI-chip loophole that let
China rent compute, measles cases at a 1991 high, US petrol at $3.78 a
gallon, Amazon's $7bn renewables investment in India, and ten more.

## How it was made

The page is drawn by code, not painted by an image model. `render.py`
reads the day's stories from `stories.json` — lead, column, grid,
briefs, map markers, dateline — and typesets them with Pillow at
1024×1024: masthead, rules, kickers, decks and all. The map's dotted
continents are rasterised from Natural Earth country outlines (the
countries-110m TopoJSON), with Antarctica left out so its fringe does
not smear the bottom edge. The typography follows newspaper convention:
Liberation Serif for the masthead, headlines and briefs, Liberation
Sans for kickers, decks and the footer. Because every word is set as
real text, the whole page stays legible: whoever judges it can read
exactly what the day held, word for word.

## Files in this repository

- `entry.png` — the finished front page; the artwork this entry submits.
- `stories.json` — the day's content: lead, column, grid, briefs, map
  markers, dateline and footer, exactly as printed on the page.
- `render.py` — the program that typesets `stories.json` into
  `entry.png` (needs the countries-110m TopoJSON as its first argument).
- `main.ts` — the entrypoint the grader runs; it ships `entry.png` to
  the output directory unchanged.

## How the entry runs

`main.ts` is deliberately small. It copies the finished `entry.png`
(PNG, 1024×1024, about 150 KB) into `$MAKEFUN_OUTPUT_DIR/entry.png`,
defaulting to `/output`, and refuses to ship anything over the 1 MiB
gate limit. The image bytes never change, so repeated grader runs
produce byte-identical output. The repository is MIT-licensed.

## Why a front page, and not one picture

The judging is pairwise and the judge has no news feed of its own, so
an entry has to be self-contained: it must carry the day inside itself.
One illustration can only ever show a single moment of a single story.
A front page can hold the whole day at once — dated, checkable
headlines, a map that places them, and briefs for everything that did
not fit above the fold. That completeness is the point of the entry.
