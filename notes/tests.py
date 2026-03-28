from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Note


class NoteModelTest(TestCase):
    def test_str(self):
        note = Note(title='My note')
        self.assertEqual(str(note), 'My note')

    def test_content_defaults_empty(self):
        note = Note.objects.create(title='No content')
        self.assertEqual(note.content, '')


class NoteAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.note = Note.objects.create(title='Test Note', content='Some content')
        self.list_url = '/api/notes/'

    def test_list_notes(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

    def test_create_note(self):
        res = self.client.post(self.list_url, {'title': 'New Note', 'content': 'Hello'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)

    def test_create_note_missing_title(self):
        res = self.client.post(self.list_url, {'content': 'No title'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_note(self):
        res = self.client.get(f'/api/notes/{self.note.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Test Note')
        self.assertIn('todos', res.data)

    def test_update_note(self):
        res = self.client.patch(f'/api/notes/{self.note.id}/', {'title': 'Updated'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated')

    def test_delete_note(self):
        res = self.client.delete(f'/api/notes/{self.note.id}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)

    def test_todos_field_is_empty_list_by_default(self):
        res = self.client.get(f'/api/notes/{self.note.id}/')
        self.assertEqual(res.data['todos'], [])
