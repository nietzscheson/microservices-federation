FROM python:3.9 as base

ARG NAME
ENV NAME=$NAME
ENV FLASK_APP=/product/src/app.py
ENV FLASK_ENV=development

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

WORKDIR /product

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

ENTRYPOINT ["sh","./entrypoint.sh" ]

CMD [ "flask run --host 0.0.0.0" ]
