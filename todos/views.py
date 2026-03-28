from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):

    serializer_class = TodoSerializer
    queryset = Todo.objects.select_related('note').all()

    