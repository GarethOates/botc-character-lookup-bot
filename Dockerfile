FROM python:3.11.6-alpine

ADD requirements.txt /

RUN pip install -r requirements.txt

ADD .env /
ADD bot.py /
ADD getCharacter.py /

CMD ["python", "./bot.py"]