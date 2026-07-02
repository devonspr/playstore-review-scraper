import argparse
from datetime import datetime

import pandas as pd
from google_play_scraper import Sort, reviews as gp_reviews

APP_ID = "com.shopee.id"


def ambil_review(count=1000, rating=None, sort=Sort.NEWEST):
    hasil, token = [], None

    while len(hasil) < count:
        batch, token = gp_reviews(
            APP_ID,
            lang="id",
            country="id",
            sort=sort,
            count=min(200, count - len(hasil)),
            filter_score_with=rating,
            continuation_token=token,
        )
        if not batch:
            break
        hasil.extend(batch)
        print(f"Terkumpul {len(hasil)}/{count} review...")
        if not token:
            break

    df = pd.DataFrame(hasil)[
        ["userName", "content", "score", "thumbsUpCount", "at"]
    ]
    return df


def main():
    p = argparse.ArgumentParser(description="Scrape review Shopee Play Store")
    p.add_argument("--count", type=int, default=1000, help="Jumlah review")
    p.add_argument("--rating", type=int, choices=range(1, 6), help="Filter rating 1-5")
    p.add_argument("--sort", choices=["newest", "best"], default="newest")
    p.add_argument("--output", type=str, default=None, help="Nama file CSV output")
    args = p.parse_args()

    sort = Sort.NEWEST if args.sort == "newest" else Sort.MOST_RELEVANT
    df = ambil_review(args.count, args.rating, sort)

    if df.empty:
        print("Tidak ada review ditemukan.")
        return

    print(f"\nTotal review : {len(df)}")
    print(f"Rata-rata    : {df['score'].mean():.2f}")


    filename = args.output or f"shopee_reviews_{datetime.now():%Y%m%d_%H%M%S}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"Disimpan ke: {filename}")


if __name__ == "__main__":
    main()
