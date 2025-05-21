# tests.py
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken


class TaskAPITestCase(APITestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Generate JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        # Initialize APIClient
        self.client = APIClient()
        
        # Set the Authorization header with the JWT token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        # Create a task for testing update and delete operations
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'Pending'
        }
        self.task = Task.objects.create(**self.task_data)

    def test_task_creation(self):
        """Test creating a task."""
        response = self.client.post('/api/tasks/', self.task_data, format='json')
        
        # Assert the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Assert that the task has been created in the database
        self.assertEqual(Task.objects.count(), 2)

    def test_get_tasks(self):
        """Test retrieving the list of tasks with pagination."""
        response = self.client.get('/api/tasks/')
        
        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert that the response contains the task created during setup
        self.assertEqual(len(response.data['results']), 1)  # Paginated to 1 result per page
        self.assertEqual(response.data['results'][0]['title'], 'Test Task')

    def test_update_task(self):
        """Test updating a task."""
        updated_data = {
            'title': 'Updated Task',
            'description': 'Updated task description',
            'status': 'In Progress'
        }
        
        response = self.client.put(f'/api/tasks/{self.task.id}/', updated_data, format='json')
        
        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reload the task from the database and assert the values have been updated
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, 'In Progress')

    def test_delete_task(self):
        """Test deleting a task."""
        response = self.client.delete(f'/api/tasks/{self.task.id}/')
        
        # Assert the response status code is 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Assert that the task is deleted from the database
        self.assertEqual(Task.objects.count(), 0)

    def test_task_not_found(self):
        """Test retrieving a task that doesn't exist."""
        response = self.client.get('/api/tasks/9999/')
        
        # Assert the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_access(self):
        """Test accessing the API without authentication."""
        
        # Remove the JWT token from the client
        self.client.credentials()

        response = self.client.get('/api/tasks/')
        
        # Assert the response status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token(self):
        """Test accessing the API with an invalid JWT token."""
        
        # Set an invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalidtoken')

        response = self.client.get('/api/tasks/')
        
        # Assert the response status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_task_creation_with_invalid_data(self):
        """Test task creation with invalid data (e.g., missing title)."""
        invalid_data = {
            'description': 'This is an invalid task',
            'status': 'Pending'
        }
        
        response = self.client.post('/api/tasks/', invalid_data, format='json')
        
        # Assert the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Assert that no task is created
        self.assertEqual(Task.objects.count(), 1)
