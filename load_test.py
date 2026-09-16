import asyncio
import time
import statistics
import httpx

URL = "http://localhost:8000/api/v1/predict"
API_KEY = "dev-secret-key-123"
TOTAL_REQUESTS = 50

payload = {
    "tenure": 12,
    "Contract": "Month-to-month",
    "InternetService": "Fiber optic",
    "MonthlyCharges": 70.5,
    "TotalCharges": 850.0,
}


async def send_request(client):
    start = time.perf_counter()

    try:
        response = await client.post(
            URL,
            headers={"X-API-Key": API_KEY},
            json=payload,
        )

        duration = time.perf_counter() - start
        return response.status_code, duration

    except Exception as e:
        duration = time.perf_counter() - start
        return f"ERROR: {e}", duration


async def main():
    async with httpx.AsyncClient(timeout=10.0) as client:
        start = time.perf_counter()

        results = await asyncio.gather(
            *[send_request(client) for _ in range(TOTAL_REQUESTS)]
        )

        total_time = time.perf_counter() - start

    successful = [r[1] for r in results if r[0] == 200]
    failed = [r for r in results if r[0] != 200]

    print("\n--- Load Test Results ---")
    print(f"Total requests : {TOTAL_REQUESTS}")
    print(f"Successful     : {len(successful)}")
    print(f"Failed         : {len(failed)}")
    print(f"Total time     : {total_time:.3f}s")

    if successful:
        print(f"Average time   : {statistics.mean(successful):.4f}s")
        print(f"Min time       : {min(successful):.4f}s")
        print(f"Max time       : {max(successful):.4f}s")

        sorted_times = sorted(successful)
        p95_index = int(len(sorted_times) * 0.95) - 1
        print(f"P95 time       : {sorted_times[p95_index]:.4f}s")

    if failed:
        print("\nFailures:")
        for failure in failed[:10]:
            print(failure)


if __name__ == "__main__":
    asyncio.run(main())
