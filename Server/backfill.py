import argparse
import asyncio

import httpx

from src.schema import Record
from src.config import server_config
from datetime import datetime, timedelta
import random

HOST = "http://localhost:8000"


def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


async def main():
    parser = argparse.ArgumentParser(description="Backfill records with random dates.")
    parser.add_argument(
        "--start_date",
        "-s",
        type=str,
        required=True,
        help="Start date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--end_date",
        "-e",
        type=str,
        required=True,
        help="End date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--count", "-n", type=int, default=10, help="Number of records to backfill"
    )
    args = parser.parse_args()

    count = args.count
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    records = []
    for _ in range(count):  # Adjust the number of records as needed
        record_date = random_date(start_date, end_date)
        record = Record(created_at=record_date, seen=True)
        records.append(record.model_dump(mode="json"))

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{HOST}/api/records/backfill/",
            headers={
                "Content-Type": "application/json",
                "api_key": server_config.auth.API_KEY,
            },
            json=records,
        )
        if response.status_code == 200:
            print(f"Backfilled {count} records")
        else:
            print(f"Failed to backfill records: {response.text}")


if __name__ == "__main__":
    asyncio.run(main())
