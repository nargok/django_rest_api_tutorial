import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import json

from unittest.mock import patch


class TestObtainAccessToken(APITestCase):
    @pytest.mark.do
    @patch('snippets.tests.access_google.sample')
    def test_mock_api_access(self, mock_func):
        # モックvalueで外部APIの通信結果をねじまげる
        mock_value = {
          "statusCode": 400,
          "ip": '127.0.0.1'
        }
        mock_func.return_value = mock_value

        url = reverse('hello_sample')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        decoded_res = json.loads(response.content.decode('utf-8'))
        print(decoded_res)
        # assert decoded_res['statusCodeFromGoogle'] == status.HTTP_200_OK
        assert decoded_res['statusCodeFromGoogle'] == status.HTTP_400_BAD_REQUEST
