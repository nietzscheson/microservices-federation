FROM python:3.9 as base

ARG NAME
ENV NAME=$NAME
ENV FLASK_APP=/app/app.py
ENV FLASK_ENV=development

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . ./

ENTRYPOINT ["sh","./entrypoint.sh" ]

CMD [ "flask run --host 0.0.0.0" ]
