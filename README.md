# Loto Libanais — Full Draw History

Every Loto Libanais draw from the first one in **September 2002** through **draw 2349
(15/09/2025)**, scraped from [lldj.com](https://www.lldj.com) into a single CSV.

The dataset is included in this repository — `loto_results.csv`, 2,349 draws — so you can use it
without running the scraper.

## The data

| Column | Description |
| --- | --- |
| `draw_number` | Sequential draw number, starting at 1 |
| `date` | Draw date, `dd/mm/yyyy` |
| `ball1` … `ball6` | The six drawn numbers, in the order the site lists them |
| `ball7` | The additional ball |
| `url` | Source page for the draw |

```csv
draw_number,date,ball1,ball2,ball3,ball4,ball5,ball6,ball7,url
1,12/09/2002,7,25,11,8,20,32,30,https://www.lldj.com/en/LatestResults/Loto?draw=1
```

## How it works

Each draw lives at a predictable URL (`?draw=N`), so the scraper walks `N` from 1 to the latest
draw, parses the page with BeautifulSoup, and pulls the numbers out of the `ball-NN` CSS classes
on the results list. Pages that return a non-200, or that yield fewer than seven balls, are
skipped and reported rather than silently dropped. There is a 0.2s pause between requests to stay
polite to the site.

## Running it

```bash
pip install -r requirements.txt
python main.py
```

Update `latest_draw` in `main.py` to the most recent draw number before running — it's currently
set to 2349. The script rewrites `loto_results.csv` from scratch and prints the status of each
draw as it goes.

## Notes

- A full run makes ~2,350 requests and takes roughly ten minutes at the current delay.
- The scraper re-fetches everything on each run; it does not resume or fetch incrementally.
- Published for anyone who wants the historical data for analysis. Draw outcomes are independent
  and uniformly random — past results have no predictive value for future draws.
