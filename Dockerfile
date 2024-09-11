FROM python:3.12-alpine

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1 

COPY . /app 

RUN pip install -r requirements.txt

CMD ["python","manage.py","runserver","0.0.0.0:8000"]

EXPOSE 8000