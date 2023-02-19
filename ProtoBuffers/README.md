## To run server
* `pip install -r requirments.txt`
* `python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. data.proto`
* `python reporting_server.py`
## In other terminal:
* `python reporting_client.py 17 45 40.0409 −29 00 28.118`
