# The World — 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/xiaokai2013/makefun-news-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/xiaokai2013/makefun-news-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-image newspaper front page summing up Saturday 21 November 2026
— built for the [make.fun bounty](https://make.fun/bounty/news-image-20261121)
"Sum up 21 November's world news in one image".

## What's on the page

Seven verified stories from the day:

1. **Russia's mass barrage on Ukraine; missiles land in Poland** — 400 drones
   and 110 missiles overnight; 8 killed in Kyiv; Warsaw calls it a
   deliberate provocation.
2. **AI sell-off drags the S&P 500 and Dow into correction** — the S&P sinks
   3.7% in a day, the Nasdaq 5.3%; Nvidia falls 14%.
3. **UK and EU sign the biggest post-Brexit deals** — three pacts on food
   trade, carbon markets and youth mobility.
4. **Saudi strikes kill 41 in Yemen as a tanker is hit in Hormuz** — Houthi
   media say 11 children are among the dead; an oil tanker is struck
   leaving the strait.
5. **Strong quake shakes Peru's Andes, felt in Lima** — residents rush into
   the streets; no casualties reported.
6. **COP31 climate talks run past deadline** — nearly 200 nations deadlocked
   over fossil fuels in Antalya.
7. **Cancer pill makes tumours vanish in trial** — daraxonrasib left cancer
   undetectable in one in 12 patients.

## How it works

- `news.json` — the seven stories, with a masthead, datelines and a
  source footer. Every headline was checked against reporting published
  on 21 November 2026.
- `render.py` — build tool (Pillow + Liberation fonts). Draws the
  1024x1024 front page and writes `entry.png`.
- `main.py` — the graded entrypoint. Standard library only: it copies the
  committed `entry.png` to `/output/entry.png`, because the grader runs
  in a bare `python:3.13-slim` container with no Pillow and no fonts.

## Rebuild

```bash
pip install Pillow
python3 render.py        # regenerates entry.png (deterministic)
python3 main.py          # copies entry.png to /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
