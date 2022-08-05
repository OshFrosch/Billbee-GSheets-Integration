# Billbee Google Sheets Integration

This repository reads and processes data from the billbee API and imports it to google sheets. The pipeline will automatically ask you to login with your Google credentials via integrating with the Google authentification serviceto be able to write to your GSheets. This pipeline will fetch live data and keep the sheet up to date.

## Setup

First create a folder named `keys`:

`mkdir keys`

And now place the `credentials.json` file in there.

Next just install requirements via:

`pip install -r requirements.txt`

And run the Pipeline via:

`python billbee_pipeline.py`
