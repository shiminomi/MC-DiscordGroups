FROM python:3.7.3

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY /app/ ./app/ 
COPY config.json .
WORKDIR /app/ 
ENTRYPOINT ["python"]
CMD ["bot.py"]
