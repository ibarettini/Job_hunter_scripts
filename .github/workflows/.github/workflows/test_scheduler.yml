name: Test Institutional Scraper

on:
  workflow_dispatch:

jobs:
  run-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install requests beautifulsoup4
      - name: Run test scraper
        run: python test_institutional_scraper.py
