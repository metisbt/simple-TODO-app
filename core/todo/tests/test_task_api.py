from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from accounts.models import User

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(email='admian@admin.com', password='2@a/1234')
    return user

# access pytest to my db
@pytest.mark.django_db
class TestPostApi:

    def test_get_post_response_200_status(self, api_client):
        url = reverse('todo:api-v1:task-list')
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_task_response_401_status(self, api_client):
        url = reverse('todo:api-v1:task-list')
        data={
            'title':'test with pytest',
            'complete':True,
            'created_date':datetime.now()
        }
        response = api_client.post(url,data)
        assert response.status_code == 401

    def test_create_task_response_201_status(self, api_client, common_user):
        url = reverse('todo:api-v1:task-list')
        data={
            'title':'test with pytest',
            'complete':True,
            'created_date':datetime.now()
        }
        user = common_user
        api_client.force_login(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_post_invalid_data_response_400_status(self, api_client, common_user):
        url = reverse('todo:api-v1:task-list')
        data={
            'complete':True,
        }
        user = common_user
        api_client.force_login(user=user)
        response = api_client.post(url,data)
        assert response.status_code == 400
