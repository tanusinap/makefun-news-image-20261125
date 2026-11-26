# News image: Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/tanusinap/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)
[![reward](https://make.fun/badge/news-image-20261125/tanusinap/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

Bounty: [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125)

One-page newspaper summing up the world news of 25 November 2026 in a
single 1024x1024 image. Built for the make.fun bounty "Sum up 25
November's world news in one image" ($100, 50 places, closes Fri 27 Nov
2026 07:00 WIB).

## Contents

- `main.py` — the generator (Python 3, Pillow, DejaVu fonts only, no
  network). Run `python3 main.py` to write `entry.png` in this directory.
- `entry.png` — the entry, 1024x1024, 185,706 bytes, sha256
  `0ffcc0efbe3314513bdb9e421fc478a6e417e4c178446f408814c41301456a33`.
  Deterministic: two runs produce identical bytes.

## The 35 stories

- **Leads:** Giza fuel tanker explosion kills 31 on Cairo's ring road;
  IRGC claims tankers hit naval mines in the Strait of Hormuz (US
  disputes it); China launches Shenzhou-24 with Pakistan's first
  astronaut, Muhammad Zeeshan Ali.
- **Secondaries:** Houthis claim a strike on Saudi Arabia's Ras Tanura
  refinery; Israel kills Hamas security chief Mohammad Abuelouf in Gaza;
  Russian strike kills two in Odesa region; RSF drone strikes kill 19
  civilians in Sudan; Solomon Islands and Australia sign a treaty
  barring foreign military bases; Nvidia reinstates Jensen Huang as CEO;
  US unveils 20-40% tariffs on 14 partners; Lille stun Bayern 2-1 and
  Liverpool win 3-0 at Club Brugge (Champions League, Matchday 5).
- **Briefs (24):** Pope Leo on COP31, Wall Street slide, CIA/ODNI breach,
  Iowa explosives disposal, Bangladesh garment wage, Spain's TV debate,
  30+ nations on chemical arms, Golden Dragon drills, Hungary-Ukraine,
  Sinner's knee surgery, Lakers win, Hong Kong fire anniversary, Riyadh
  condemnation, Alice Huang, Wang Yi in The Hague and London, Taipei
  comedian, UK AI warning, airports funding, London Museum, Tokyo data
  centres, Canada student curbs, Barcelona 4-1 Sabah.
- **Region counts:** ASIA 7, EUROPE 10, AMERICAS 8, AFRICA 2,
  MIDDLE EAST 4, OCEANIA 1, GLOBAL 3.
- **DATE CHECK box** names the excluded stories: 24 Nov (Huawei's US
  conviction, the Riyadh tower strike, Champions League day one),
  23 Nov (Wellington Test draw, Spain's Puigdemont amnesty), 22 Nov
  (COP31 collapse, the Bahrain strikes, El Chapo Isidro captured).

## Verification notes

- Every story was checked against web sources dated 25 November 2026
  (Just Security Early Edition, Reuters via BusinessWorld, UEFA, Xinhua,
  Wikipedia for the Giza explosion). No story from another date is
  included; the DATE CHECK box names the near-miss stories.
- Two items were deliberately hedged: the Hormuz mine claim (sources
  disagree on how many tankers were hit: 2, 3 or 4, so no count is
  given) and the Champions League (the Wednesday-night set per UEFA's
  25 Nov round-up was used; the Tuesday set belongs to 24 Nov).
- The India-New Zealand Wellington Test draw happened on Monday 23 Nov,
  so it is excluded even though reports about it were published on 25 Nov.

## Submission (not done by this build)

Build-only. make.fun entries are code: this folder's `main.py` +
`entry.png` must be put in a public GitHub repo with `main.py` at the
root and an OSI LICENSE, then the repo/commit link is pasted on
make.fun and the entry is wallet-signed. That step needs Sultan (repo
creation + signature). Handed-over entries rank but cannot win cash
prizes; they count toward the $MAKE airdrop activity.
