FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# RUN pip install fastapi uvicorn

CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]



