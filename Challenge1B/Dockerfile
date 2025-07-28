FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY script.py ./
COPY challenge1b_input.json ./
COPY pdfs ./pdfs

CMD ["python", "script.py", "--input", "challenge1b_input.json", "--pdf_dir", "pdfs", "--output", "output.json"]
