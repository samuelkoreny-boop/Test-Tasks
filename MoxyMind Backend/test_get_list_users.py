import requests
import pytest

URL = "https://reqres.in"

#Saved last names of first two users
first_user = "Lawson"
second_user = "Ferguson"

def test_case_1():
    response = requests.get(f"{URL}/api/users?page=2")

    assert response.status_code == 200

    body = response.json()

    #Verify "total" and first two "last_name" entries in "data
    assert "total" in body

    assert body["data"][0]["last_name"] == first_user
    assert body["data"][1]["last_name"] == second_user

    #Comparing the number of users and "total" value will result in a failed test since this is the second page which shows only half of total users
    user_count = len(body["data"])
    total_value = body["total"]
    #assert user_count == total_value

    #Comparing the "per_page" would result in a correct comparison as that is the actual number of users in "data" on this page
    per_page = body["per_page"]
    assert user_count == per_page

    #Or there is an option to compare the "total" value with number of users in a higher or equal relationship
    assert total_value >= user_count

    #Verify data types of
    for user in body["data"]:
        assert isinstance(user["id"], int)
        assert isinstance(user["email"], str)
        assert isinstance(user["first_name"], str)
        assert isinstance(user["last_name"], str)
        assert isinstance(user["avatar"], str)