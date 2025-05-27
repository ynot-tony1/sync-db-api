FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8002
CMD ["uvicorn", "db_api.main:app", "--host", "0.0.0.0", "--port", "8002"]
