# Trading Automations

Requirements

- Python 3.9+
- tesseract-ocr (on MacOS: `brew install tesseract`)
- wkhtmltopdf (on MacOS: `brew install wkhtmltopdf`)

To run this project you need to run this commands.

```bash
python -m venv ~/.envs/trading-automations
source ~/.envs/trading-automations/bin/activate
pip install -r requirements.txt

# Process Options Snapshots
python process_options_snapshots.py
# Enter the path to the options snapshots file
```
