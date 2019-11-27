FROM python:3
ENV PYTHONUNBUFFERED 1
#RUN mkdir dockerdjango
WORKDIR /news_site
COPY requirements.txt .
RUN ls -l
RUN pip install -r ./requirements.txt
COPY . /news_site