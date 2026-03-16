FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY README.md ./README.md
COPY ARCHITECTURE.md ./ARCHITECTURE.md
COPY INTERVIEW_GUIDE.md ./INTERVIEW_GUIDE.md

ENV PYTHONPATH=/app/src
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "fab_sim.api:app", "--host", "0.0.0.0", "--port", "8000"]
