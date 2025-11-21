import requests
import pytest
import json
from jsonschema import validate
from datetime import datetime

URL = "https://reqres.in"

#Maximum response time of 1000 ms
response_time = 1000

#New user data taken from provided .json file
with open("test_data.json") as f:
    test_data = json.load(f)

#Response schema for validation
response_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "id": {"type": "string"},
        "createdAt": {"type": "string"},
    },
    "required": ["name", "job", "id", "createdAt"]
}

#This posts all the users one by one from the provided .json file
@pytest.mark.parametrize("data", test_data)
def test_case_2(data):

    #Provided API KEY from reqres.in
    headers = {"x-api-key": "reqres-free-v1"}

    response = requests.post(f"{URL}/api/users", json=data, headers=headers)

    assert response.status_code == 201

    body = response.json()

    #Verify id and createdAt fields and the value of id and correct format of timestamp
    assert "id" in body and body["id"]
    assert "createdAt" in body
    assert datetime.fromisoformat(body["createdAt"].replace("Z", "+00:00"))

    #Compares actual runtime in ms and maximum response time defined in a variable
    response_time_ms = response.elapsed.total_seconds() * 1000
    assert response_time_ms < response_time

    #Validates response schema based on predefined schema
    validate(instance=body, schema=response_schema)