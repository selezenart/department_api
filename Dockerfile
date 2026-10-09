FROM python:3.8

RUN useradd --create-home userapi
WORKDIR /departmentsProject

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ .
RUN chown -R userapi:userapi ./
USER userapi

ENV PORT=5000
EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
