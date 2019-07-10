import requests
from snippets.tests.access_google import sample

# def sample():
#     try:
#         res = requests.get("http://checkip.amazonaws.com/")
#     except requests.RequestException as e:
#         print(e)
#         raise e
#     return {
#         "statusCode": res.status_code,
#         "ip": res.text
#     }

# pytest-mockを使った例
def test_mock_sample(mocker):
    response_mock = mocker.Mock()
    response_mock.status_code = 404
    response_mock.text = '127.0.0.1'

    mocker.patch('requests.get').return_value = response_mock

    actual = sample()
    assert actual['statusCode'] == 404
    assert actual['ip'] == '127.0.0.1'
