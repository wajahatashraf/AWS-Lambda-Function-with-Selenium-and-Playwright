#!/bin/bash
set -e

latest_stable_json="https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
json_data=$(curl -s "$latest_stable_json")

chrome_url=$(echo "$json_data" | jq -r '.channels.Stable.downloads.chrome[0].url')
driver_url=$(echo "$json_data" | jq -r '.channels.Stable.downloads.chromedriver[0].url')

mkdir -p /opt/chrome /opt/chrome-driver

curl -Lo /tmp/chrome.zip $chrome_url
unzip -q /tmp/chrome.zip -d /opt/chrome
rm -f /tmp/chrome.zip

curl -Lo /tmp/chromedriver.zip $driver_url
unzip -q /tmp/chromedriver.zip -d /opt/chrome-driver
rm -f /tmp/chromedriver.zip
