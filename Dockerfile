FROM python:3.7.8

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api /app/api

EXPOSE 8000
CMD ["uvicorn","api.main:app","--host=0.0.0.0","--reload"]