<p align="center">
  <img src="z.svg" alt="UpTimeRobot logo" width="300">
</p>

# UpTimeRobot

**Lightweight uptime and keep-alive service designed to help prevent free-tier apps on platforms like Render, Koyeb, Heroku and other hosting services from going idle or sleeping.**

**It periodically sends requests to your configured app URLs to keep them active and provides a simple web API for monitoring their status.**

## Features

- **Automatic endpoint health checks**
- **Configurable ping interval**
- **Response time tracking**
- **Endpoint status and statistics**
- **Simple health/status API**
- **Supports multiple `.txt` files for URLs**
- **One-click deployment support**
- **Lightweight and easy to self-host**

## Configuration

You can add URLs directly to `alive.py`:

```python
ENDPOINTS = [
    "https://your-app.example.com",
]
```

Or create any `.txt` file in the root directory and add one URL per line:

```text
https://your-app.koyeb.app
https://your-app.onrender.com
https://yourdomain.com
```

The application automatically scans all `.txt` files in the root directory and adds every valid `http://` or `https://` URL.

Both methods can be used together.

<details>
  <summary><strong>Variables</strong></summary>

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Web server port |
| `PING_TIME` | `300` | Health check interval in seconds |
| `REQUEST_TIMEOUT` | `10` | Request timeout in seconds |

</details>

<details>
  <summary><strong>API</strong></summary>

### Health Check

```text
/health
```

Returns a simple health response.

### Status

```text
/status
```

Returns the current status of all monitored endpoints, including response time, status code, success count and failure count.

### Root

```text
/
```

Returns service information and overall monitoring status.

</details>

<details>
  <summary><strong>Deployment</strong></summary>

<br>

<details>
  <summary><strong>Render (One-Click Deploy)</strong></summary>

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ImKrishana/UpTimeRobot&branch=main)

</details>

<details>
  <summary><strong>Koyeb (One-Click Deploy)</strong></summary>

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&builder=buildpack&repository=github.com/ImKrishana/UpTimeRobot&branch=main&name=uptime-robot&service_type=web&ports=8080%3Bhttp%3B%2F)

</details>

<details>
  <summary><strong>Heroku (One-Click Deploy)</strong></summary>

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ImKrishana/UpTimeRobot/tree/main)

</details>

<details>
  <summary><strong>VPS / Locally</strong></summary>

```bash
git clone https://github.com/ImKrishana/UpTimeRobot.git
cd UpTimeRobot
pip install -r requirements.txt
python alive.py
```

The web server will start on the port specified by `PORT`.

</details>

</details>

<details>
  <summary><strong>Disclaimer</strong></summary>

This bot is developed strictly for **educational and research purposes only**.

</details>

---

[![License](https://img.shields.io/github/license/ImKrishana/UpTimeRobot)](https://github.com/ImKrishana/UpTimeRobot/blob/main/LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?logo=telegram&logoColor=white)](https://t.me/LeechBots)

If you like this project, don't forget to give it a Star !

**Developer:** [The Zake](https://t.me/TheZake)
