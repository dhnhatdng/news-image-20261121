[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/dhnhatdng/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![Reward](https://make.fun/badge/news-image-20261121/dhnhatdng/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

# news-image-20261121

One image that sums up the world's news of Saturday, 21 November 2026,
drawn as a newspaper front page.

The lead story is the one first reported on the day: Russian missiles
coming down in Poland during a massive overnight assault on Ukraine,
which Warsaw called a deliberate provocation and NATO condemned as a
grave violation of Polish airspace. The page also carries the fallout
from the week's biggest verdict, the ICJ finding Myanmar guilty of
genocide against the Rohingya, plus a US sentencing, a claimed proof
of the Riemann Hypothesis, the COP31 talks running out of road, and
the day's other headlines.

## How it is built

`draw_frontpage.py` draws the page with Pillow from the verified
stories and saves it as `entry.png` (1024 by 1024). `main.py` is the
entry program: it copies that image to the output directory the
grader provides.

```sh
python3 draw_frontpage.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Every fact on the page was checked against wire and major-outlet
reporting from 21 November 2026: AP, Al Jazeera, UN News, Le Monde
and The Times.
