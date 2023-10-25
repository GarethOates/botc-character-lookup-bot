FROM python:3.11.6-alpine

ADD requirements.txt /

RUN pip install -r requirements.txt

ADD .env /
ADD main.py /
ADD get_character.py /

CMD ["python", "./main.py"]