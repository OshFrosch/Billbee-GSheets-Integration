# Billbee Google Sheets Integration

This repository reads and processes data from the billbee API and imports it to google sheets with modular authentification. The SetUp is exeptionally easy reagarding Google. You just have to LogIn via your Google Account.

## Setup

First create a folder named `keys`:

`mkdir keys`

And now place the `credentials.json` file in there.

Next just install requirements via:

`pip install -r requirements.txt`

And run the Pipeline via:

`python billbee_pipeline.py`
