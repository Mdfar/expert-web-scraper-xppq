FROM mcr.microsoft.com/playwright/python:v1.40.0-focal

WORKDIR /app COPY requirements.txt . RUN pip install --no-cache-dir -r requirements.txt RUN playwright install chromium

COPY . .

CMD ["python", "scraper/stealth_engine.py"]