import asyncio
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from aiohttp import ClientSession, ClientTimeout, web

ENDPOINTS = [
    "https://your-app.koyeb.app",
    "https://your-app.onrender.com",
]

PORT = int(os.getenv("PORT", 8080))
PING_TIME = int(os.getenv("PING_TIME", 300))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))

START_TIME = time.monotonic()

def load_endpoints():
    endpoints = list(ENDPOINTS)

    for txt_file in Path(".").glob("*.txt"):
        try:
            with txt_file.open("r", encoding="utf-8") as file:
                for line in file:
                    url = line.strip()

                    if url.startswith(("http://", "https://")):
                        endpoints.append(url)

        except OSError as error:
            print(f"[ERROR] Failed to read {txt_file}: {error}")

    return list(dict.fromkeys(endpoints))
    
ALL_ENDPOINTS = load_endpoints()

endpoint_status = {
    url: {
        "status": "pending",
        "status_code": None,
        "response_time_ms": None,
        "last_checked": None,
        "success_count": 0,
        "failure_count": 0,
        "error": None,
    }
    for url in ALL_ENDPOINTS
}


def uptime():
    return int(time.monotonic() - START_TIME)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


async def _start_web():
    routes = web.RouteTableDef()

    @routes.get("/", allow_head=True)
    async def root(request):
        healthy = all(
            data["status"] == "up"
            for data in endpoint_status.values()
        )

        return web.json_response({
            "status": "healthy" if healthy else "degraded",
            "service": "Uptime Robot",
            "uptime_seconds": uptime(),
            "endpoint_count": len(ALL_ENDPOINTS),
            "ping_interval_seconds": PING_TIME,
            "request_timeout_seconds": REQUEST_TIMEOUT,
            "last_checked": max(
                (
                    data["last_checked"]
                    for data in endpoint_status.values()
                    if data["last_checked"]
                ),
                default=None,
            ),
            "developer": {
                "name": "TheZake",
                "github": "https://github.com/ImKrishana",
                "telegram": "https://t.me/TheZake",
            },
        })

    @routes.get("/health", allow_head=True)
    async def health(request):
        return web.json_response({
            "status": "ok",
            "service": "Uptime Robot",
        })

    @routes.get("/status", allow_head=True)
    async def status(request):
        return web.json_response({
            "status": "online",
            "service": "Uptime Robot",
            "uptime_seconds": uptime(),
            "ping_interval_seconds": PING_TIME,
            "endpoints": endpoint_status,
        })

    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app, access_log=None)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    print(f"[INFO] Uptime Robot started on port {PORT}")
    print(f"[INFO] Monitoring {len(ALL_ENDPOINTS)} endpoint(s)")
    print(f"[INFO] Ping interval: {PING_TIME}s")
    print(f"[INFO] Request timeout: {REQUEST_TIMEOUT}s")

    if ALL_ENDPOINTS:
        for url in ALL_ENDPOINTS:
            source = "ENDPOINTS" if url in ENDPOINTS else "TXT"
            print(f"[INFO] Added [{source}] {url}")


async def _ping():
    await asyncio.sleep(60)

    timeout = ClientTimeout(total=REQUEST_TIMEOUT)

    async with ClientSession(timeout=timeout) as session:
        while True:
            print("[INFO] Starting health check...")

            for url in ALL_ENDPOINTS:
                started = time.monotonic()

                try:
                    async with session.get(url) as response:
                        elapsed = round(
                            (time.monotonic() - started) * 1000,
                            2,
                        )

                        data = endpoint_status[url]

                        data["status"] = (
                            "up"
                            if 200 <= response.status < 400
                            else "down"
                        )
                        data["status_code"] = response.status
                        data["response_time_ms"] = elapsed
                        data["last_checked"] = utc_now()
                        data["error"] = None

                        if data["status"] == "up":
                            data["success_count"] += 1
                        else:
                            data["failure_count"] += 1

                        print(
                            f"[PING] {url} -> "
                            f"{response.status} "
                            f"({elapsed} ms)"
                        )

                except Exception as error:
                    data = endpoint_status[url]

                    elapsed = round(
                        (time.monotonic() - started) * 1000,
                        2,
                    )

                    data["status"] = "down"
                    data["status_code"] = None
                    data["response_time_ms"] = elapsed
                    data["last_checked"] = utc_now()
                    data["failure_count"] += 1
                    data["error"] = type(error).__name__

                    print(
                        f"[ERROR] {url} -> "
                        f"{type(error).__name__}: {error}"
                    )

            print(f"[INFO] Next health check in {PING_TIME}s")
            await asyncio.sleep(PING_TIME)


async def main():
    print("[INFO] Initializing Uptime Robot...")
    await asyncio.gather(
        _start_web(),
        _ping(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[INFO] Uptime Robot stopped")
