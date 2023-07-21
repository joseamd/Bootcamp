FROM python:3.9

WORKDIR .

ADD ./FinishingSchool/requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt
RUN pip install django-environ

RUN mkdir -p /app/

COPY ./FinishingSchool /app/

WORKDIR /app/

EXPOSE 8000

CMD ["python","manage.py", "runserver", "0.0.0.0:8000"]
