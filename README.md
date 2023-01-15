# Example code of moto-based DynamoDB with FastAPI 

Japanese version is [here](). 

This repository represents how to develop FastAPI based API Service with mocking by [moto](https://docs.getmoto.org/en/latest/docs/services/dynamodb.html). 

- main.py: Represents FastAPI and pynamodb-based model config 
- test_main.py: Represents test codes by moto and starlette testing client

If you check this, please type these on your console.

```bash 
$ poetry install 
$ poetry run python -m unittest test_main.py
```