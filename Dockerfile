FROM python:3.11-alpine
RUN mkdir /usr/med_course_bot
WORKDIR /usr/med_course_bot
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
EXPOSE 443
EXPOSE 80
COPY . .
ENV PYTHONPATH="${PYTHONPATH}:/usr/med_course_bot/bot"