# The RPC Server

## Generate Python code from the protobufs
```shell

# person_rpc
python3 -m grpc_tools.protoc -I ./protobufs --python_out=./modules/person_rpc/app --grpc_python_out=./modules/person_rpc/app ./protobufs/*.proto

# connection
python3 -m grpc_tools.protoc -I ./protobufs --python_out=./modules/connection --grpc_python_out=./modules/connection ./protobufs/*.proto

```

## The RPC Client
```shell

```

```
flask run --host 0.0.0.0
```

```shell

# location

curl -X POST \
  http://localhost:5001/api/locations \
  -H 'Content-Type: application/json' \
  -d '{
  "latitude": "-122.290524",
  "longitude": "37.553441",
  "creation_time": "2020-08-18T10:37:06",
  "person_id": 29
}'


curl -X POST \
  http://localhost:5000/api/locations \
  -H 'Content-Type: application/json' \
  -d '{
  "latitude": "-122.290524",
  "longitude": "37.553441",
  "creation_time": "2020-08-18T10:37:06",
  "person_id": 29
}'


# person
curl -X POST \
  http://localhost:5001/api/persons \
  -H 'Content-Type: application/json' \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "ABC Corp"
  }'


  curl -X POST \
  http://localhost:5001/api/persons \
  -H 'Content-Type: application/json' \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "ABC Corp"
  }'

```

```shell

bin/kafka-topics.sh --create --topic location-topic --bootstrap-server localhost:9092

bin/kafka-console-consumer.sh --topic location-topic --from-beginning --bootstrap-server localhost:9092


bin/kafka-topics.sh --create --topic person-topic --bootstrap-server localhost:9092

bin/kafka-console-consumer.sh --topic person-topic --from-beginning --bootstrap-server localhost:9092

```