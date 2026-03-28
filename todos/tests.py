from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from notes.models import Note
from .models import Todo


class TodoModelTest(TestCase):
    def test_str(self):
        todo = Todo(title='Buy milk', status='pending')
        self.assertEqual(str(todo), '[pending] Buy milk')

    def test_default_status_is_pending(self):
        todo = Todo.objects.create(title='Task')
        self.assertEqual(todo.status, Todo.Status.PENDING)


class TodoAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.note = Note.objects.create(title='My Note')
        self.todo = Todo.objects.create(title='First Task', note=self.note)
        self.list_url = '/api/todos/'

    def test_list_todos(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

    def test_create_todo_without_note(self):
        res = self.client.post(self.list_url, {'title': 'Standalone task'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(res.data['note_detail'])

    def test_create_todo_with_note(self):
        res = self.client.post(self.list_url, {'title': 'Linked task', 'note': self.note.id}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['note_detail']['id'], self.note.id)

    def test_create_todo_with_invalid_note(self):
        res = self.client.post(self.list_url, {'title': 'Bad note', 'note': 9999}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_todo_has_note_detail(self):
        res = self.client.get(f'/api/todos/{self.todo.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['note_detail']['title'], 'My Note')

    def test_note_field_is_write_only(self):
        # 'note' (raw FK) should NOT appear in the response
        res = self.client.get(f'/api/todos/{self.todo.id}/')
        self.assertNotIn('note', res.data)

    def test_update_status(self):
        res = self.client.patch(f'/api/todos/{self.todo.id}/', {'status': 'done'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.status, 'done')

    def test_unlink_note_sets_null(self):
        res = self.client.patch(f'/api/todos/{self.todo.id}/', {'note': None}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertIsNone(self.todo.note)

    def test_deleting_note_does_not_delete_todo(self):
        # on_delete=SET_NULL — todo should survive note deletion
        self.note.delete()
        self.todo.refresh_from_db()
        self.assertIsNone(self.todo.note)
        self.assertTrue(Todo.objects.filter(id=self.todo.id).exists())


class CrossAppTest(TestCase):
    """Tests that validate the bidirectional relationship works correctly."""

    def setUp(self):
        self.client = APIClient()

    def test_note_shows_linked_todos(self):
        note = Note.objects.create(title='Note with todos')
        Todo.objects.create(title='Task A', note=note)
        Todo.objects.create(title='Task B', note=note)
        res = self.client.get(f'/api/notes/{note.id}/')
        self.assertEqual(len(res.data['todos']), 2)
        titles = [t['title'] for t in res.data['todos']]
        self.assertIn('Task A', titles)
        self.assertIn('Task B', titles)
