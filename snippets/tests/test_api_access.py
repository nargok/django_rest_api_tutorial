import requests
import json
import jsonpath

import pytest

# APIテストのサンプルコード
@pytest.mark.skip
def test_add_student_data():
  API_URL = "http://thetestingworldapi.com/api/studentsDetails"

  student = dict(first_name="taro", middle_name=None, last_name="yamada", date_of_birth="1978/01/01")
  response = requests.post(API_URL, student)
  assert response.status_code == 201

  json_response = json.loads(response.text)
  first_name = jsonpath.jsonpath(json_response, 'first_name')
  assert first_name[0] == "taro"

@pytest.mark.skip
def test_get_student_data():
  API_URL = "http://thetestingworldapi.com/api/studentsDetails/58"

  response = requests.get(API_URL)
  json_response = json.loads(response.text)
  id = jsonpath.jsonpath(json_response, 'data.id')
  assert id[0] == 58