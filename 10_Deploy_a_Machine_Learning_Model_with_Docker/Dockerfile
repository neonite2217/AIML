# 4. Write Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY model.pkl .

# 6. Test using /docs Swagger UI
# Command to run the container:
# docker build -t housing-predictor .
# docker run -d -p 8000:8000 housing-predictor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
