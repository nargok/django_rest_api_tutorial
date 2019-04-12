import request
import json
import jsonpath


def test_add_student_data():
  API_URL = "http://thetestingworldapi.com/api/studentsDetails"

  # crete object
  json_request = json.loads(object)
  response = request.post(API_URL, json_request)

  print(response.text)