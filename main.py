import requests
from bs4 import BeautifulSoup
import csv
import time
import re

BASE_URL = "https://www.lldj.com/en/LatestResults/Loto?draw={}"
OUT_CSV = "loto_results.csv"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def parse_draw(draw_no):
    url = BASE_URL.format(draw_no)
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")

    date_text = ""
    span = soup.select_one("span.draw")
    if span:
        m = re.search(r"(\d{2}/\d{2}/\d{4})", span.get_text())
        if m:
            date_text = m.group(1)

    balls = []
    for li in soup.select("ul.ballslist li"):
        cls = " ".join(li.get("class",[]))
        m = re.search(r"ball-(\d{1,2})", cls)
        if m:
            balls.append(int(m.group(1)))
    if len(balls) < 7:
        return None

    return {
        "draw_number": draw_no,
        "date":date_text,
        "ball1": balls[0],
        "ball2": balls[1],
        "ball3": balls[2],
        "ball4": balls[3],
        "ball5": balls[4],
        "ball6": balls[5],
        "ball7": balls[6],
        "url": url
    }


def main():
    latest_draw = 2349 # this should be updated with the latest draw
    rows = []

    for draw in range(1,latest_draw+1):
        data = parse_draw(draw)
        if data:
            rows.append(data)
            print(f"Draw {draw} OK")
        else:
            print(f"Draw {draw} FAILED")
        time.sleep(0.2)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["draw_number","date","ball1","ball2","ball3","ball4","ball5","ball6","ball7","url"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} rows to {OUT_CSV}")

if __name__ == "__main__":
    main()