FROM python:3.7-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5006

CMD ["python", "location_ingester.py"]