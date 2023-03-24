FROM python:3.11 as base

ENV FLASK_DEBUG=true

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

WORKDIR /services

COPY requirements.txt ./

RUN pip install -r requirements.txt

FROM base as user

ARG NAME
ENV NAME=$NAME
ENV FLASK_APP=/services/user/src/app.py

WORKDIR /services/user

CMD flask run --host 0.0.0.0

FROM base as product

ARG NAME
ENV NAME=$NAME
ENV FLASK_APP=/services/product/src/app.py

WORKDIR /services/product

CMD flask run --host 0.0.0.0

FROM base as order

ARG NAME
ENV NAME=$NAME
ENV FLASK_APP=/services/order/src/app.py

WORKDIR /services/order

CMD flask run --host 0.0.0.0
