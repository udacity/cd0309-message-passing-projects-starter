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