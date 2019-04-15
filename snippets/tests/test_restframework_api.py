import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

from django.contrib.auth.models import User


class TestObtainAccessToken(APITestCase):
  @pytest.mark.django_db
  def test_cat_get_access_token(self):
    User.objects.create_superuser('admin_user', 'admin_user@example.com', 'password')

    self.valid_payload = {
      'username': 'admin_user',
      'password': 'password',
    }

    url = reverse('obtain_jwt_token')
    response = self.client.post(url,
                                data=json.dumps(self.valid_payload),
                                content_type='application/json')

    assert response.status_code == status.HTTP_200_OK