FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /news-site
COPY requirements.txt .
RUN ls -l
RUN pip install -r ./requirements.txt
COPY . /news-site