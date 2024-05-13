import sys
import time
import random
import configparser
import requests
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_config():
    """Read and parse the configuration file."""
    config = configparser.ConfigParser()
    config.read('categories.ini')
    return config

def get_weighted_category(config):
    """Return a category based on the specified weights."""
    categories = config.get("categories", "categories").split(",")
    weights = [int(config.get(cat, 'weight')) for cat in categories]
    return random.choices(categories, weights)[0]  # Uses weighted selection.

def run_simulation(category, config):
    """Simulate traffic for a given category."""
    user_agent = config.get(category, 'user_agent')
    ip_address = config.get(category, 'ip_address')

    headers = {
        "Cache-Control": "no-cache",
        "User-Agent": user_agent,
        "X-Source-Ip": ip_address
    }
    url = "https://www.fastlylab.com"  # Change to actual URL path as needed.

    response = requests.get(url, headers=headers, verify=False)
    print(f"Request to {category}: {response.status_code} - {response.reason}")

    time.sleep(random.randint(1, 10))

def main():
    config = read_config()
    try:
        while True:
            selected_category = get_weighted_category(config)
            run_simulation(selected_category, config)
    except KeyboardInterrupt:
        print("Simulation stopped by user.")

if __name__ == "__main__":
    main()
