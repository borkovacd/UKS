FROM python:3.6
MAINTAINER olgaSavic

ENV PYTHONUNBUFFERED=1

RUN pip install -U pip setuptools
RUN pip install --upgrade pip

RUN mkdir /scm_project
WORKDIR /scm_project

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]

