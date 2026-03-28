from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):

    todos = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'todos']
        read_only_fields = ['id','created_at', 'updated_at']
    
    def get_todos(self, obj):
        return [
            {
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'status': todo.status,
                'created_at': todo.created_at
            }
            for todo in obj.todos.all()
        ]

class NoteMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title']