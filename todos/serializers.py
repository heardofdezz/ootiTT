from rest_framework import serializers
from .models import Todo
from notes.serializers import NoteMinimalSerializer

class TodoSerializer(serializers.ModelSerializer):

    note_detail = NoteMinimalSerializer(source='note' ,read_only=True)

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'status', 'created_at','note_detail', 'note', 'updated_at']
        read_only_fields = ['id','created_at', 'updated_at']
        
        extra_kwargs = {
            'note': {'write_only': True, 'required': False, 'allow_null': True},
        }
    