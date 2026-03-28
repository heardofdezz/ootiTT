from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import Note
from .serializers import NoteSerializer

class NoteViewSet(viewsets.ModelViewSet):

    serializer_class = NoteSerializer
    queryset = Note.objects.prefetch_related('todos').all()