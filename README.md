# Tibber Price Alert

This script fetches hourly electricity prices from the Tibber API and sends a push notification via Pushover if any price for the next day (including taxes) is negative. It includes a retry mechanism for fetching prices and is intended to be run daily (e.g., via cron).

## Features
- Fetches tomorrow's hourly prices from Tibber using GraphQL and your personal access token
- Checks for negative prices (with taxes)
- Sends a high-priority push notification to a Pushover device group if negative prices are found
- Retries price fetching up to 3 times on failure
- Uses a `.env` file for configuration

## Requirements
- Python 3.8+
- A Tibber personal access token ([get one here](https://developer.tibber.com/docs/getting-started))
- A Pushover application token and group key ([get one here](https://pushover.net/))

## Setup

1. **Clone the repository or copy the files**

2. **Create and activate a virtual environment:**

```sh
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```sh
pip install -r requirements.txt
```

4. **Configure environment variables:**

Copy `.env.example` to `.env` and fill in your credentials:

```
TIBBER_TOKEN=your_tibber_token
PUSHOVER_TOKEN=your_pushover_app_token
PUSHOVER_GROUP=your_pushover_group_key
```

5. **Run the script:**

```sh
python tibber_price_alert.py
```

If negative prices are found for tomorrow, a push notification will be sent to your Pushover group.

## Scheduling (Optional)
To run the script automatically every day (e.g., at 13:00), add a cron job:

```
0 13 * * * /path/to/your/venv/bin/python /path/to/tibber_price_alert.py
```

## Customization
- The script currently only checks for negative prices for "tomorrow". You can adjust the `find_negative_prices` function to include today if needed.
- The notification message and priority can be customized in the `send_push_notification` function.
