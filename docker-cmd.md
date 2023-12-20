```shell

# connection
sudo docker build -t kydq2022/nd064-c2-connection-api:latest modules/connection
sudo docker push kydq2022/nd064-c2-connection-api:latest

# location
sudo docker build -t kydq2022/nd064-c2-location-api:latest modules/location
sudo docker push kydq2022/nd064-c2-location-api:latest

sudo docker build -t kydq2022/nd064-c2-location-consumer:latest modules/location_consumer
sudo docker push kydq2022/nd064-c2-location-consumer:latest


# person
sudo docker build -t kydq2022/nd064-c2-person-api:latest modules/person
sudo docker push kydq2022/nd064-c2-person-api:latest

sudo docker build -t kydq2022/nd064-c2-person-consumer:latest modules/person_consumer
sudo docker push kydq2022/nd064-c2-person-consumer:latest

sudo docker build -t kydq2022/nd064-c2-person-rpc:latest modules/person_rpc
sudo docker push kydq2022/nd064-c2-person-rpc:latest

sudo docker build -t kydq2022/nd064-c2-udaconnect-app:latest modules/frontend
sudo docker push kydq2022/nd064-c2-udaconnect-app:latest

```

```
sudo docker run -p 5000:5001 \
  -e DB_USERNAME="ct_admin" \
  -e DB_NAME="geoconnections" \
  -e DB_PASSWORD="wowimsosecure" \
  -e DB_HOST="localhost" \
  -e DB_PORT="5432" \
  -e GRPC_SERVER_ADDRESS="localhost:50051" \
  -e KAFKA_BOOTSTRAP_SERVERS="localhosxt:9092" \
  kydq2022/nd064-c2-location-api:latest

```